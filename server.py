from pathlib import Path
from mcp.server.fastmcp import FastMCP

from db import run_query

mcp = FastMCP("Assistant MCP")


@mcp.tool()
def save_note(content: str, tag: str | None = None) -> str | None:
    try:
        run_query("INSERT INTO notes (content, tag) VALUES (?, ?)", (content, tag))
        return f"Saved noted: {content} ([tag: {tag}])"
    except Exception as e:
        print(f"Error saving note: {e}")
        return None


@mcp.tool()
def get_notes(limit: int = 10) -> list[dict]:
    try:
        rows = run_query(
            "SELECT id, content, tag, created_at FROM notes ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )

        return [dict(r) for r in rows]
    except Exception as e:
        print(f"Error getting notes: {e}")
        return []


@mcp.tool()
def search_notes(query: str) -> list[dict]:
    try:
        rows = run_query(
            "SELECT id, content, tag, created_at FROM notes WHERE content LIKE ? ORDER BY created_at DESC",
            (f"%{query}%",),
        )
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"Error searching notes: {e}")
        return []


@mcp.tool()
def delete_note(note_id: int) -> str | None:
    try:
        run_query("DELETE FROM notes where id = ? ", (note_id,))
        return f"Deleted note {note_id}"
    except Exception as e:
        print(f"Error deleting note {note_id}: {e}")
        return None


@mcp.tool()
def add_reminder(content: str, remind_at: str | None = None) -> str | None:
    try:
        run_query(
            "INSERT INTO reminders (content, remind_at) VALUES (?,?)",
            (content, remind_at),
        )
        result = f"Reminder set: {content}"
        if remind_at:
            result += f" (at: {remind_at})"
        return result
    except Exception as e:
        print(f"Error adding reminder: {e}")
        return None


@mcp.tool()
def get_reminders(include_done: bool = False) -> list[dict]:
    query = "SELECT id, content, remind_at, done, created_at FROM reminders"
    if not include_done:
        query += " WHERE done = 0"
    query += " ORDER BY created_at DESC"
    try:
        rows = run_query(query)
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"Error getting reminders: {e}")
        return []


@mcp.tool()
def complete_reminder(reminder_id: int) -> str | None:
    try:
        rows = run_query(
            "UPDATE reminders SET done = 1 WHERE id = ? RETURNING *", (reminder_id,)
        )
        if rows:
            return f"Reminder {reminder_id} marked as done"
        return f"No reminder found with ID {reminder_id}"
    except Exception as e:
        print(f"Error completing reminder: {e}")
        return None


if __name__ == "__main__":
    mcp.run()
