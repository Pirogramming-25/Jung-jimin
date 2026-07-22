from functools import wraps
from urllib.parse import urlencode

from django.shortcuts import redirect


def login_required_with_message(view_func):
    """
    로그인하지 않은 사용자가 접근하면
    로그인 페이지로 이동시키고 required=1을 전달합니다.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            query_string = urlencode({
                "next": request.get_full_path(),
                "required": "1",
            })

            return redirect(f"/accounts/login/?{query_string}")

        return view_func(request, *args, **kwargs)

    return wrapper