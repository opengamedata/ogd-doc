# Segment Tab

In the segment tab, you segment data, so multiple rows belong to the same segment.

Table of contents
- [Manual segmenting](#manual-segmenting)
- [Automatic segmenting](#automatic-segmenting)

**IMPORTANT**: the following operations **overwrite** the **affected** segments' labels. You can lose your progress, **download dataset before experimenting**.

## Manual segmenting
We select the **user** from the dropdown (events from different users will never be inside one segment) that also displays the **number of segments**.

Then you have to **select the rows** that you want to apply a `segment_id` value. Apart from just clicking, you can drag and scroll with the mouse, use **Click and Shift** for faster multiple events selection.

After selecting, you can set the **Segment Id** and hit **Apply**. The segment is saved to the `segment_id` column.

## Automatic segmenting
To make segmenting much faster (or at least the prior segmenting in bigger segments), you can use the **Cutoff Event Types**.

Basically, the segments are formed by "cutting" the dataframe in segments using those rows that have an `event_name` **value among the selected** as the **dividers**. This cutoff event itself goes into the previous segment after dividing.

In addition, **if** the **new session** is started, it also goes to a **new segment**. So there are no different sessions events in the same segment, even if the user is the same.