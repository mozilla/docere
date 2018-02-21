# Implementation Notes

* Build
  * Collect metadata
    * Provides read-only access to the KR
  * Meta-report plugins
    * Provide the KR as a directory for input
    * Examples:
      * blog index
      * rss feed
      * markdown renderer
  * Fails if:
    * Insufficient metadata according to plugins
      * publish_date
      * author
    * Plugin checks
* Push KR to repo as-is
  * Push to s3 functionality
