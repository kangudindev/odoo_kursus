/** @odoo-module **/

import { registry } from "@web/core/registry";
import { CharField } from "@web/views/fields/char/char_field";
import { useInputField } from "@web/views/fields/input_field_hook";

export class TextTransformWidget extends CharField {
    setup() {
        super.setup();

        useInputField({
            getValue: () => this.props.value || "",
            parse: (value) => {
                const mode = this.props.options?.mode || "none";

                if (mode === "upper") {
                    return value.toUpperCase();
                }
                if (mode === "lower") {
                    return value.toLowerCase();
                }
                if (mode === "capital") {
                    return value.replace(/\b\w/g, c => c.toUpperCase());
                }
                return value;
            },
        });
    }
}

registry.category("fields").add("text_transform", TextTransformWidget);
