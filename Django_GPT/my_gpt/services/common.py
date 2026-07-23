import torch


def get_pipeline_device():
    """Hugging Face pipeline에서 사용할 장치를 반환합니다."""

    if torch.cuda.is_available():
        return 0

    if (
        hasattr(torch.backends, "mps")
        and torch.backends.mps.is_available()
    ):
        return torch.device("mps")

    return -1