You write test questions for a search benchmark over Indonesian regulations.

Below are several pasal (articles). Each has an id and its text. For EACH pasal, write 1 or 2 questions
that a non-lawyer would type into a search box to find the rule in that pasal. Think of an HR officer,
a small-business owner, a company director, an employee, or a BPJS participant.

Rules for every question:
- Plain, natural Indonesian, 8 to 30 words, as a real person would ask it.
- The pasal must answer it. Ask about the specific rule in this pasal, not about the topic in general.
- Do not copy any run of 3 or more words from the pasal. Use your own words. Standard terms that
  have no other name are allowed (for example "BPJS Ketenagakerjaan", "Penghasilan Tidak Kena Pajak",
  "Rapat Umum Pemegang Saham", "Jaminan Hari Tua").
- Do not name the regulation, its number, or the pasal number.
- One type per question: definisi, kewajiban, hak, angka (a rate, amount, deadline or period),
  prosedur, sanksi, larangan.
- If a pasal has no rule a person would ask about (it only refers to another rule, only says a
  later regulation will set the details, or only says something was deleted), write no question for it.

Answer with JSON only, no other text:
{"items": [{"unit_id": "<id>", "questions": [{"q": "<question>", "type": "<type>"}]}]}

PASAL:
