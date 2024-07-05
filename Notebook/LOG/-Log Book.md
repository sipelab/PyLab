
> [!TABLE] Log
> ```dataview
TABLE file.mtime as "Created"
WHERE date(LOG) = date(this.file.name)
SORT file.mtime desc
>```

