# Custom Search

streaming custom search command that shows information about youtube videos based on squid proxy logs

## Syntax

source="*squid*" uri="*www.youtube.com/watch?v=*" | sort _time | youtube uri | table _time clientip uri youtube

