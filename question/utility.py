import json

import requests

from .serializers import *

URL = "https://leetcode.com/graphql"


def createProblem(slug):
    import markdownify as md
    payload = {
        "operationName": "questionData",
        "variables": {"titleSlug": slug},
        "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    title    titleSlug    content     difficulty    similarQuestions    exampleTestcases        topicTags {      name      slug   }    hints    sampleTestCase     }}"}
    headers = {
        "content-type": "application/json",
    }
    response = requests.request("GET", URL, json=payload, headers=headers)
    content = json.loads(response.content.decode("utf-8"))["data"]["question"]
    problem = Problem()
    problem.problem_name: str = content["title"]
    problem.problem_slug: str = content['titleSlug']
    problem.difficulty: str = content['difficulty']
    problem.topic: str = content['topicTags'][0]["name"]
    topicTags: list = content['topicTags']
    problem.related_topics: dict = {}
    for i in topicTags:
        problem.related_topics["name"] = i['name']
        problem.related_topics["slug"] = i['slug']
    html: str = content["content"]
    html = f"<h3>{content['title']}</h3>" + html
    problem.markdown: str = md.markdownify(html, heading_style="ATX")
    problem.save()
    return problem


def getProblemsSortedByTopics():
    problems = Problem.objects.all()
    topics = []
    result = {}
    for problem in problems:
        topics.append(problem.topic)
    for topic in topics:
        problem = Problem.objects.filter(topic=topic)
        problemS = ProblemSerializer(problem, many=True)
        result[topic] = problemS.data
    return result


def getProblemSortedbyDifficulty():
    difficulty: list = ['Easy', 'Medium', 'Hard']
    result = {}
    for i in difficulty:
        problem = Problem.objects.filter(difficulty=i)
        problemS = ProblemSerializer(problem, many=True)
        result[i] = problemS.data
    return result
