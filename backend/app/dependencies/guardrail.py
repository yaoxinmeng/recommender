import boto3
from loguru import logger

from app.core.config import settings

class GuardrailException(BaseException): ...

guardrail_client = boto3.client("bedrock-runtime")

def apply_guardrail(text: str, is_input: bool = True) -> None:
    """
    Apply guardrail on a piece of text. Raises a `GuardrailException` if 
    the guardrail intervened.

    :param str text: The text to be analyzed
    :param bool is_input: Whether the text is a user input or a model output
    :return None: Does not return anything, but will raise `GuardrailException` if 
    the guardrail intervened.
    """
    response = guardrail_client.apply_guardrail(
        guardrailIdentifier=settings.BEDROCK_GUARDRAIL_ID,
        guardrailVersion=settings.BEDROCK_GUARDRAIL_VERSION,
        source='INPUT'if is_input else 'OUTPUT',
        content=[
            {
                'text': {
                    'text': text
                }
            },
        ]
    )
    action = response.get("action")
    if action == "GUARDRAIL_INTERVENED":
        reasons = response.get("assessments")
        raise GuardrailException(f"Guardrails intervened: {reasons}")