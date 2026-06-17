import re
import os
import logging

logger = logging.getLogger('duplicati-monitor')


def lookup_dot_separated_key(data, key):
    value = data

    for k in key.split('.'):
        if k in value:
            value = value[k]
        else:
            value = "---"
            logger.warning(f"Key {key} not found")

    return value


def generate_message_report(data):
    default_template_error = os.getenv("TEMPLATE_ERROR", "💾 🔴 Backup failed: <Extra.backup-name>\n- Status: <Data.ParsedResult>\n⏱ Duration: <Data.Duration>\n- Files examined: <Data.ExaminedFiles>")
    default_template_success = os.getenv("TEMPLATE_SUCCESS", "💾 🟢 Backup successful: <Extra.backup-name>\n- Files examined: <Data.ExaminedFiles>\n- New files: <Data.AddedFiles>\n⏱ Duration: <Data.Duration>\n- Status: <Data.ParsedResult>")
    
    if "TestResults" not in data["Data"] or "ParsedResult" not in data["Data"]["TestResults"] \
            or data["Data"]["TestResults"]["ParsedResult"] != "Success":
        message = default_template_error

    else:
        message = default_template_success

    # Split template
    template_split = re.split("([<>])", message)
    i = 0

    for s in template_split:
        i += 1

        if s == "<":
            message = message.replace(f"<{template_split[i]}>", str(lookup_dot_separated_key(data, template_split[i])))

    return message
