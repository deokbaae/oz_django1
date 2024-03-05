import json
from http.client import BAD_REQUEST
from json import JSONDecodeError

from django.http import HttpRequest, JsonResponse
from django.views import View

from services import create_comment_service

# Create your views here.


class CommentView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        errors = []

        try:
            body = json.loads(request.body)
        except JSONDecodeError:
            errors.append("JSON 형식이 아닙니다.")

        if "article_id" not in body:
            errors.append("article_id 가 없습니다.")
        elif not isinstance(body["article_id"], int):
            errors.append(f"article_id 는 정수 여야 합니다. 전달된 값: {body['article_id']}")
        if "author" not in body:
            errors.append("author 가 없습니다.")
        elif not isinstance(body["author"], str):
            errors.append(f"author 는 문자열 여야 합니다. 전달된 값: {body['author']}")
        if "body" not in body:
            errors.append("body 가 없습니다.")
        elif not isinstance(body["body"], str):
            errors.append(f"body 는 문자열 여야 합니다. 전달된 값: {body['body']}")

        if errors:
            return JsonResponse({"errors": errors}, status=BAD_REQUEST)

        comment = create_comment_service(
            body["article_id"],
            body["author"],
            body["body"],
        )
        return JsonResponse({"comment_id": comment.id})
