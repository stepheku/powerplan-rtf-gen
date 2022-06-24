"""
plan_csv_to_dict.py
~~~~~~~~~~~~~~~~~~~

Converts the PowerPlan CSV into a hierarchical dictionary
"""

import utils.general as general
from pathlib import Path
import csv

# STRING_ENCODING = "utf-8-sig"


def create_order_comments_dict(input_file: str) -> dict:
    order_comments_dict = {}
    with open(
        Path(input_file),
        mode="r",
    ) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            order_sentence_id = row.get("ORDER_SENTENCE_ID").strip()
            order_comments_dict[order_sentence_id] = row.get("ORDER_COMMENTS")

    return order_comments_dict


def create_powerplan_comp_dict(input_file: str, order_comments_file: str) -> dict:
    fields_for_iv_sets = [
        "IV_SYNONYM",
        "ORDER_SENTENCE_SEQ",
        "ORDER_SENTENCE_ID",
        "ORDER_SENTENCE_DISPLAY_LINE",
        "ORDER_COMMENTS",
    ]

    order_comments_dict = create_order_comments_dict(order_comments_file)
    components_dict = {}
    with open(input_file, mode="r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            comp_path_cat_id = float(row.get("PATHWAY_CATALOG_ID").strip())
            pathway_comp_id = float(row.get("PATHWAY_COMP_ID").strip())
            iv_synonym = row.get("IV_SYNONYM").strip()
            order_sentence_id = row.get("ORDER_SENTENCE_ID").strip()

            if comp_path_cat_id not in components_dict:
                components_dict[comp_path_cat_id] = {}

            if pathway_comp_id not in components_dict[comp_path_cat_id]:
                components_dict[comp_path_cat_id][pathway_comp_id] = {
                    k: v.strip()
                    for k, v in row.items()
                    if not k.startswith("ORDER_SENTENCE")
                    and not k.startswith("IV_SYNONYM")
                }
                components_dict[comp_path_cat_id][pathway_comp_id][
                    "TIME_ZERO_IND"
                ] = int(
                    components_dict[comp_path_cat_id][pathway_comp_id][
                        "TIME_ZERO_IND"
                    ].strip()
                )

                components_dict[comp_path_cat_id][pathway_comp_id]["SEQUENCE"] = int(
                    components_dict[comp_path_cat_id][pathway_comp_id]["SEQUENCE"]
                )

                if not iv_synonym:
                    components_dict[comp_path_cat_id][pathway_comp_id][
                        "ORDER_SENTENCES"
                    ] = []
                    components_dict[comp_path_cat_id][pathway_comp_id][
                        "ORDER_SENTENCES"
                    ].append(
                        {
                            k: v.strip()
                            for k, v in row.items()
                            if k.startswith("ORDER_SENTENCE")
                        }
                    )

                else:
                    components_dict[comp_path_cat_id][pathway_comp_id][
                        "IV_COMPONENTS"
                    ] = []
                    components_dict[comp_path_cat_id][pathway_comp_id][
                        "IV_COMPONENTS"
                    ].append(
                        {
                            k: v.strip()
                            for k, v in row.items()
                            if k in fields_for_iv_sets
                        }
                    )
                    iv_order_sentence_id = components_dict[comp_path_cat_id][
                        pathway_comp_id
                    ]["IV_COMPONENTS"][-1].get("ORDER_SENTENCE_ID")
                    if iv_order_sentence_id in order_comments_dict:
                        components_dict[comp_path_cat_id][pathway_comp_id][
                            "IV_COMPONENTS"
                        ][-1]["ORDER_COMMENTS"] = order_comments_dict[
                            iv_order_sentence_id
                        ]

            else:
                # additional order_sentence_id for the same component
                if int(row.get("ORDER_SENTENCE_SEQ").strip()) > 1:
                    components_dict[comp_path_cat_id][pathway_comp_id][
                        "ORDER_SENTENCES"
                    ].append(
                        {
                            k: v.strip()
                            for k, v in row.items()
                            if k.startswith("ORDER_SENTENCE")
                        }
                    )

                # otherwise, is an IV set component
                else:
                    components_dict[comp_path_cat_id][pathway_comp_id][
                        "IV_COMPONENTS"
                    ].append(
                        {
                            k: v.strip()
                            for k, v in row.items()
                            if k in fields_for_iv_sets
                        }
                    )

            if order_sentence_id in order_comments_dict and not iv_synonym:
                components_dict[comp_path_cat_id][pathway_comp_id]["ORDER_SENTENCES"][
                    -1
                ]["ORDER_COMMENTS"] = order_comments_dict[order_sentence_id]

    return components_dict


def create_powerplan_dict(
    input_file: str, components_file: str, order_comments_file: str
) -> dict:
    components_dict = create_powerplan_comp_dict(
        input_file=components_file, order_comments_file=order_comments_file
    )
    powerplan_dict = {}
    with open(input_file, mode="r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            pathway_catalog_id = float(row.get("PATHWAY_CATALOG_ID").strip())
            phase_pathway_catalog_id = float(
                row.get("PHASE_PATHWAY_CATALOG_ID").strip()
            )
            if pathway_catalog_id not in powerplan_dict:
                powerplan_dict[pathway_catalog_id] = {
                    k: v.strip() for k, v in row.items() if not k.startswith("PHASE")
                }

                powerplan_dict[pathway_catalog_id]["PHASES"] = {}

            if phase_pathway_catalog_id != 0:
                powerplan_dict[pathway_catalog_id]["PHASES"][
                    phase_pathway_catalog_id
                ] = {k: v.strip() for k, v in row.items() if k.startswith("PHASE")}
                powerplan_dict[pathway_catalog_id]["PHASES"][phase_pathway_catalog_id][
                    "COMPONENTS"
                ] = components_dict.get(phase_pathway_catalog_id)

            else:
                powerplan_dict[pathway_catalog_id]["COMPONENTS"] = components_dict.get(
                    pathway_catalog_id
                )

            if (
                pathway_catalog_id not in components_dict
                and phase_pathway_catalog_id not in components_dict
            ):
                powerplan_dict.pop(pathway_catalog_id)

    return powerplan_dict


def csv_to_dict(input_file: str = None):
    # input_file = remove_invalid_chars_from_csv_first_line(input_file)
    powerplan_dict = create_powerplan_dict(input_file)
    return powerplan_dict


if __name__ == "__main__":
    powerplan_dict = create_powerplan_dict(
        input_file="./pathways.csv",
        components_file="./components.csv",
        order_comments_file="./order_comments.csv",
    )
    # import json
    # with open("sample.json", "w") as f:
    #     json.dump(powerplan_dict[2608000941], f)