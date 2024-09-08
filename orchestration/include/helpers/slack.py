import os
import urllib

from slack_sdk.webhook import WebhookClient


def send_notification(context: dict) -> None:
    """
    Send a Slack notification with the specified details.

    :param context: context of the DAG
    """

    url = os.getenv("SLACK_WEBHOOK")
    client = WebhookClient(url)

    execution_date = context["ts"]
    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    title = f"Task {task_id} of DAG {dag_id} has failed"
    message = (
        context["exception"]
        if "exception" in context
        else "Click the button below to check the logs"
    )
    client = WebhookClient(url)
    text = f"{title}: {message}"

    log_params = urllib.parse.urlencode(
        {"dag_id": dag_id, "task_id": task_id, "execution_date": execution_date}
    )

    dag_url = f"http://localhost:8080/log?{log_params}"
    message_blocks = get_message_block(dag_id, dag_url, title, message)
    client.send(text=text, blocks=message_blocks)


def get_message_block(
    dag_id: str, dag_url: str, title: str, message: str
) -> list[dict]:
    """
    Generate a Slack message block with details for the notification.

    :param dag_id: Identifier for the Directed Acyclic Graph (DAG).
    :param dag_url: URL for accessing the DAG details.
    :param title: Title of the notification.
    :param message: Message content of the notification.
    :return: A list of dictionaries representing Slack message blocks.
    """
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f":red_circle: " f"{title}",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Dag: *`{dag_id}`*",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{message}*",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Dag status: *`Failed`*",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Check Dag (login first)",
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Open"},
                "value": "open_resource",
                "url": f"{dag_url}",
                "action_id": "button-action",
            },
        },
    ]
