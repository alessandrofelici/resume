---
trigger: always_on
---

Do not edit the files under ./saved-resumes or ./sections. Only edit draft.tex.

Significant numbers should be bolded when drafting a sample .tex file for a resume.

The length of the resume should be one page. It should take up as much space as possible without going over one page.

When revising sentences, make them more concise and impactful. Use strong action verbs and quantify achievements whenever possible. The sentences should take up the full line they are given, without extending only a few words into the next line. Given this, do not forcefully extend a sentence.

Do not make up any statistics. If you do not know a statistic, say "Not Applicable" or "N/A". Ask the user if a statistic is suggested based on the content of the sentence, or the requirements of the given job.

Do not use any emojis or special characters. Only use standard text characters.

Do not use any LaTeX packages that are not already installed. You can check the installed packages by running `pdflatex --version`.

The purpose of this program is to use a given url for a computer science related internship and generate a resume for it. The resume should be tailored to the given url. The resume should be saved as a .tex file in draft.tex. The resume should be generated using the given url and the user's information. The user's information should be stored in the ./sections directory.

Drafted sentences will be marked with an asterisk. Consult the user for changes to these sentences. Do not remove the astrisk, only the user should.