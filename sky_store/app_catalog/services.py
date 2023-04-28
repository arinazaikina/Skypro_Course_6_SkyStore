from .models import Feedback


class FeedbackServices:
    @classmethod
    def save_feedback(cls, name: str, phone: str, message: str) -> None:
        feedback = Feedback(name=name, phone=phone, message=message)
        feedback.save()
