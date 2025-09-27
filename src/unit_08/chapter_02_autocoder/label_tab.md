# Label Tab

In the label tab, you perform qualitative analysis and assign labels for specific behaviours identified in the segment

Table of contents
- [Navigation](#navigation)
- [Labeling](#labeling)

## Navigation
We select the **user** from the dropdown, but we also have the [<<] [>>] buttons to change the selected user.

Also, we have the **segments dropdown**, that can be modified with [<] [>]. The dropdown also displays the segment label (if any) and the job the user was in when segment started.

## Labeling
You can either **create a new label** when typing and hitting enter or either select from existing labels.

The user can provide a **description for each label** either using the pencil button to edit existing or just importing a codebook that can look like this:

```json
[
    {
        "code": "Struggle",
        "definition": "Indicates moments when a player encounters significant difficulty in completing a job."
    },
    {
        "code": "No Struggle",
        "definition": "Applied when a player progresses through a task smoothly without evident setbacks."
    }
]
```

Also, you can use the **Justification** control to make notes on why you chose that label.

After hitting **Apply**, the information is saved to the `segment_labels` column.

After applying, the top section **Labels count** updates after recounting.