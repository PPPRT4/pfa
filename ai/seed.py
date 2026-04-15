from notes_ai import ajouter_note
import os
import shutil

if __name__ == "__main__":
    print("Seeding the database with Second Brain notes...\n")

    notes_to_add = [
        {"id": "note_1", "texte": "Book Summary - Atomic Habits: The core idea is that getting 1% better every day leads to massive compounding results over time. Focus on systems, not goals."},
        {"id": "note_2", "texte": "Project Idea - AI Assistant: Build a local AI assistant using LangGraph and Llama 3 that can search through my local markdown files and summarize them."},
        {"id": "note_3", "texte": "Meeting Notes - Q3 Planning: The main goals for Q3 are to increase user retention by 15% and successfully launch the new iOS mobile app."},
        {"id": "note_4", "texte": "Tech Snippet - Docker: To completely clear all unused Docker containers, networks, images, and volumes, use the command 'docker system prune -a --volumes'."},
        {"id": "note_5", "texte": "Personal Goal: Train for the Carthage Marathon in 2026. Need to run at least 3 times a week and do one long run on Sundays."},
        {"id": "note_6", "texte": "Travel Plans - Japan: Planning a trip to Kyoto and Tokyo in October. Must visit the Fushimi Inari Shrine and try authentic Wagyu beef."},
        {"id": "note_7", "texte": "Quote - Naval Ravikant: 'Play iterated games. All the returns in life come from compound interest.'"},
        {"id": "note_8", "texte": "Recipe - Perfect Pizza Dough: 500g flour, 325ml warm water, 10g salt, 3g yeast. Ferment 48 hours."},
        {"id": "note_9", "texte": "Tech Snippet - Git: git reset --soft HEAD~1 keeps changes staged."},
        {"id": "note_10", "texte": "Finance - Monthly Rules: Keep groceries under 400 TND. Invest 20% monthly."},
        {"id": "note_11", "texte": "Workout Routine - PPL split: Push, Pull, Legs weekly cycle."},
        {"id": "note_12", "texte": "Watchlist: Dune Part Two, Severance."},
        {"id": "note_13", "texte": "Japanese basics: Arigatou = thank you, Sumimasen = sorry/excuse me."},
        {"id": "note_14", "texte": "Home Maintenance: Change AC filter every 3 months."},
        {"id": "note_15", "texte": "Gift Ideas: Kindle Paperwhite or ceramic pots."},
        {"id": "note_16", "texte": "1-on-1: Improve communication, lead backend project."},
        {"id": "note_17", "texte": "V60 Coffee: 15g coffee, 250ml water, 2:30 brew time."},
        {"id": "note_18", "texte": "Stoicism: Focus only on what is in your control."},
    ]

    for note in notes_to_add:
        ajouter_note(note["id"], note["texte"])

    print("\n🎉 Database seeded successfully!")
    