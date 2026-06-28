# Maintenance

Recurring house tasks — filters, batteries, whole-unit replacements (alarms), seasonal
work. The `reminders.md` playbook reads the schedule plus `items/` to surface what's due.

Start from [`schedule.template.md`](schedule.template.md): copy it to `schedule.md`
(gitignored) and fill in your tasks. Each task carries an interval, a last-done date, a
computed next-due, and a **cited source** for the interval.

**Rule:** don't invent intervals. An interval without a source stays `TODO` until the
overnight loop confirms it from a manual or manufacturer page.

> Your real `schedule.md` is gitignored — only this README and the template are tracked.
