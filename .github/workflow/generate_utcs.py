import json
import os


def add_effected_actions(template: str, info: dict) -> str:
    template += "\n#### Effected Actions:\n"
    template += "- [ ] All\n"
    template += "- [ ] Check Health\n"

    actions = info.get("operations", [])
    for action in actions:
        template += f"- [ ] {action.get('title')}\n"
    if not actions:
        template += "_Add changes impact here_\n"
    return template


def add_unit_test_cases(template: str, info: dict) -> str:
    template += "\n#### UTCs:\n"

    template += \
        "- [ ] Connector installation verified.\n" \
        "- [ ] Connector logo verified.\n" \
        "- [ ] Docs link verified.\n" \
        "- [ ] Actions and Playbooks list verified.\n" \
        "- [ ] Playbooks tags verified.\n" \
        "- [ ] All playbooks are in info mode verified.\n" \
        "- [ ] All playbooks are in inactive mode verified.\n" \
        "- [ ] Ingestion playbooks are verified.\n" \
        "- [ ] Check health verified.\n"

    actions = info.get("operations", [])
    for action in actions:
        template += f"- [ ] {action.get('title')} action verified.\n"
    return template


def read_info(info_file_path: str) -> dict:
    file = open(info_file_path, "r")
    info = json.load(file)
    file.close()
    return info


def get_info_file_path():
    info_file_path = None
    for dirname, dirnames, filenames in os.walk('.'):
        if dirname in [".git", ".github"]:
            continue
        if "info.json" in filenames:
            info_file_path = dirname + "/info.json"
            break
    return info_file_path


def create_template(info: dict) -> str:
    template = ""
    template = add_effected_actions(template, info)
    template = add_unit_test_cases(template, info)
    return template


def write_template(output_path: str, template: str) -> None:
    template_file_path = os.path.join(output_path, "pull_request_template.md")

    file = open(template_file_path, "w")
    file.write(template)
    file.close()


def main() -> None:
    info_file_path = get_info_file_path()
    if info_file_path is None:
        raise Exception("info.json not found.")
    info = read_info(info_file_path)
    template = create_template(info)
    print(template)


if __name__ == '__main__':
    main()
