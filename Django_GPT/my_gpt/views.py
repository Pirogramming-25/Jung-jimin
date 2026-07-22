import json
import logging

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .decorators import login_required_with_message
from .models import InferenceHistory
from .services.combo import analyze_combo
from .services.moderator import analyze_toxicity
from .services.sentiment import analyze_sentiment
from .services.summarizer import summarize_text


logger = logging.getLogger(__name__)


def get_recent_histories(request, task):
    if not request.user.is_authenticated:
        return []

    return InferenceHistory.objects.filter(
        user=request.user,
        task=task,
    )[:5]


def is_english_text(text):
    return text.isascii() and any(
        character.isalpha() for character in text
    )


def parse_json_request(request):
    try:
        return json.loads(request.body), None
    except json.JSONDecodeError:
        return None, JsonResponse(
            {
                "ok": False,
                "error": "올바르지 않은 요청입니다.",
            },
            status=400,
        )


def create_history_response(history):
    return {
        "input": history.input_text,
        "result": history.result,
        "created_at": history.created_at.isoformat(),
    }


def home(request):
    return redirect("sentiment")


# --------------------------------------------------
# 감정 분석
# --------------------------------------------------

def sentiment(request):
    context = {
        "recent_histories": get_recent_histories(
            request,
            InferenceHistory.Task.SENTIMENT,
        ),
    }

    return render(
        request,
        "my_gpt/sentiment.html",
        context,
    )


@require_POST
def sentiment_run(request):
    data, error_response = parse_json_request(request)

    if error_response:
        return error_response

    text = data.get("text", "").strip()

    if not text:
        return JsonResponse(
            {
                "ok": False,
                "error": "분석할 문장을 입력해 주세요.",
            },
            status=400,
        )

    if len(text) > 1000:
        return JsonResponse(
            {
                "ok": False,
                "error": "문장은 1000자 이하로 입력해 주세요.",
            },
            status=400,
        )

    if not is_english_text(text):
        return JsonResponse(
            {
                "ok": False,
                "error": "영어 문장만 입력할 수 있습니다.",
            },
            status=400,
        )

    try:
        result = analyze_sentiment(text)
        history_data = None

        if request.user.is_authenticated:
            history = InferenceHistory.objects.create(
                user=request.user,
                task=InferenceHistory.Task.SENTIMENT,
                input_text=text,
                result=result,
            )

            history_data = create_history_response(history)

        return JsonResponse(
            {
                "ok": True,
                "result": result,
                "history": history_data,
            }
        )

    except Exception:
        logger.exception(
            "감정 분석 처리 중 오류가 발생했습니다."
        )

        return JsonResponse(
            {
                "ok": False,
                "error": (
                    "감정 분석 중 오류가 발생했습니다. "
                    "잠시 후 다시 시도해 주세요."
                ),
            },
            status=500,
        )


# --------------------------------------------------
# 문서 요약
# --------------------------------------------------

@login_required_with_message
def summarize(request):
    context = {
        "recent_histories": get_recent_histories(
            request,
            InferenceHistory.Task.SUMMARIZE,
        ),
    }

    return render(
        request,
        "my_gpt/summarize.html",
        context,
    )


@require_POST
@login_required_with_message
def summarize_run(request):
    data, error_response = parse_json_request(request)

    if error_response:
        return error_response

    text = data.get("text", "").strip()

    if len(text) < 100:
        return JsonResponse(
            {
                "ok": False,
                "error": "100자 이상 입력해 주세요.",
            },
            status=400,
        )

    if len(text) > 5000:
        return JsonResponse(
            {
                "ok": False,
                "error": "5000자 이하로 입력해 주세요.",
            },
            status=400,
        )

    if not is_english_text(text):
        return JsonResponse(
            {
                "ok": False,
                "error": "영어 문서만 입력할 수 있습니다.",
            },
            status=400,
        )

    try:
        result = summarize_text(text)

        history = InferenceHistory.objects.create(
            user=request.user,
            task=InferenceHistory.Task.SUMMARIZE,
            input_text=text,
            result=result,
        )

        return JsonResponse(
            {
                "ok": True,
                "result": result,
                "history": create_history_response(history),
            }
        )

    except Exception:
        logger.exception(
            "문서 요약 처리 중 오류가 발생했습니다."
        )

        return JsonResponse(
            {
                "ok": False,
                "error": (
                    "요약 중 오류가 발생했습니다. "
                    "잠시 후 다시 시도해 주세요."
                ),
            },
            status=500,
        )


# --------------------------------------------------
# 유해 표현 분석
# --------------------------------------------------

@login_required_with_message
def moderate(request):
    context = {
        "recent_histories": get_recent_histories(
            request,
            InferenceHistory.Task.MODERATE,
        ),
    }

    return render(
        request,
        "my_gpt/moderate.html",
        context,
    )


@require_POST
@login_required_with_message
def moderate_run(request):
    data, error_response = parse_json_request(request)

    if error_response:
        return error_response

    text = data.get("text", "").strip()

    if not text:
        return JsonResponse(
            {
                "ok": False,
                "error": "문장을 입력해 주세요.",
            },
            status=400,
        )

    if len(text) > 1000:
        return JsonResponse(
            {
                "ok": False,
                "error": "1000자 이하로 입력해 주세요.",
            },
            status=400,
        )

    if not is_english_text(text):
        return JsonResponse(
            {
                "ok": False,
                "error": "영어 문장만 입력할 수 있습니다.",
            },
            status=400,
        )

    try:
        result = analyze_toxicity(text)

        history = InferenceHistory.objects.create(
            user=request.user,
            task=InferenceHistory.Task.MODERATE,
            input_text=text,
            result=result,
        )

        return JsonResponse(
            {
                "ok": True,
                "result": result,
                "history": create_history_response(history),
            }
        )

    except Exception:
        logger.exception(
            "유해 표현 분석 처리 중 오류가 발생했습니다."
        )

        return JsonResponse(
            {
                "ok": False,
                "error": (
                    "유해 표현 분석 중 오류가 발생했습니다. "
                    "잠시 후 다시 시도해 주세요."
                ),
            },
            status=500,
        )


# --------------------------------------------------
# 복합 분석
# --------------------------------------------------

@login_required_with_message
def combo(request):
    context = {
        "recent_histories": get_recent_histories(
            request,
            InferenceHistory.Task.COMBO,
        ),
    }

    return render(
        request,
        "my_gpt/combo.html",
        context,
    )


@require_POST
@login_required_with_message
def combo_run(request):
    data, error_response = parse_json_request(request)

    if error_response:
        return error_response

    text = data.get("text", "").strip()

    if not text:
        return JsonResponse(
            {
                "ok": False,
                "error": "문장을 입력해 주세요.",
            },
            status=400,
        )

    if len(text) > 5000:
        return JsonResponse(
            {
                "ok": False,
                "error": "5000자 이하로 입력해 주세요.",
            },
            status=400,
        )

    if not is_english_text(text):
        return JsonResponse(
            {
                "ok": False,
                "error": "영어 문장만 입력할 수 있습니다.",
            },
            status=400,
        )

    try:
        result = analyze_combo(text)

        history = InferenceHistory.objects.create(
            user=request.user,
            task=InferenceHistory.Task.COMBO,
            input_text=text,
            result=result,
        )

        return JsonResponse(
            {
                "ok": True,
                "result": result,
                "history": create_history_response(history),
            }
        )

    except Exception:
        logger.exception(
            "복합 분석 처리 중 오류가 발생했습니다."
        )

        return JsonResponse(
            {
                "ok": False,
                "error": (
                    "복합 분석 중 오류가 발생했습니다. "
                    "잠시 후 다시 시도해 주세요."
                ),
            },
            status=500,
        )