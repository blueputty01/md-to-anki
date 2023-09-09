# Google Doc to Anki 📄

Imports Google Doc into Anki (spaced repetition software) to keep memory of notes fresh.

# How to use 🤔

1. Create a Google Doc using the guidelines below
2. Download the Google Doc as a zipped HTML file and run the code with modifications based on the file name location

## Features ⚒️

* Nested lists
* Bold/italics
* Images
* Uses [anki-connect](https://github.com/FooSoft/anki-connect#media-actions) to automatically add parsed data to Anki

## Example ❔

### Input text:

All notes are imported with the cloze type. Underlined text are converted to cloze fields. Breaks between notes refer to
new fields, and indented text refer to text in the extra field. Title text is converted to the tags field.

> The <ins>Articles of Confederation</ins> defined the government that ran the American Revolution.
>
> * Land Ordinance Act of 1785
>     * allowed federal government to sell western lands
>         * pay off national debt
>         * organize new lands into townships and public schools
> * Northwest Ordinance of 1787
>     * provided that when new territory reached population of 60K → could apply for statehood with no slavery allowed
> 
> <ins>Shay’s Rebellion</ins> was when farmers struggled to pay their taxes post American Revolution
> 
> * 1786
> * crushed by Massachusetts state militia
> * watershed moment for new government

### Outputted note 1:

Text: 
> The {{c1::Articles of Confederation}} defined the government that ran the American Revolution.

Extra:

> * Land Ordinance Act of 1785
>     * allowed federal government to sell western lands
>         * pay off national debt
>         * organize new lands into townships and public schools
> * Northwest Ordinance of 1787
>     * provided that when new territory reached population of 60K → could apply for statehood with no slavery allowed