# Overview

An important part of the Open Learning Platform is the ability to host open learning materials created by members of the community, in the hopes of sharing this information with the wider water science community. After contributing and becoming an author on the Open Learning Platform, individuals are able to request an Authorship Impact Report that summarizes user analytics collected by Heap on the pages that they contributed. The information in the report can be used in resumes, CVs, tenure packages, or any other instances where they would want to communicate the impact and reach of their work.

# Instructions on generating authorship impact reports

Instructions for generating the Authorship Impact Report can be found below. It is important to note that the code to generate the reports lives in the [engagement data harmonization repository](https://github.com/CUAHSI/engagement-data-harmonization). This code will eventually be extracted and moved into it's own GitHub repository.

There is some specific information needed from authors when requesting an ad-hoc Authorship Impact Report.

-   The date range they would like the data to cover
-   What pages they contributed to the Open Learning Platform

## Retrieving analytics exports from Heap

There are two data sets that need to be generated with Heap and downloaded as CSVs. The names of these files should be prefixed with the date range requested by the author. This date range should be formatted as `YYMMDD_YYMMDD`. For example, if an author requests data from January 1st, 2026 to September 1st, 2026, the date range would be formatted as `260101_260901`.

To begin, first navigate to https://www.heap.io/ and log in. If you do not have credentials to CUAHSI's account on Heap, contact Martin Seul. After logging in, make sure that that the `Apps` tab in the bottom left is selected to `Water Content Portal` so that you can see user analytics specifically for the open learning pages. 

Below are details for generating each Heap export:

- **User analytics grouped by country:** 
    - [Use this link](https://heapanalytics.com/app/env/902525459/pages/chart/Region-specific-analytics-complete-country-19332860) to navigate to the chart containing page-level engagement by country for first time page viewers in a given time range
    - Under `Filter Results`, change the date range as per the author's request
    - Click `Export` and `Export Result to CSV`
    - Save exported file as `YYMMDD_YYMMDD_heap_analytics_country.csv` replacing `YYMMDD_YYMMDD` with the date range of interest as described above
    - `YYMMDD_YYMMDD_heap_analytics_country.csv`
- **User analytics grouped by region (e.g., US state):**
    - [Use this link](https://heapanalytics.com/app/env/902525459/pages/chart/Region-specific-analytics-19302305) to navigate to the chart containing page-level engagement by region for first time page viewers in a given time range
    - Under `Filter Results`, change the date range as per the author's request
    - Click `Export` and `Export Result to CSV`
    - Save exported file as `YYMMDD_YYMMDD_heap_analytics_region.csv` replacing `YYMMDD_YYMMDD` with the date range of interest as described above

## Generating the authorship impact report locally

The Authorship Impact Report is generated using the pipeline package `targets` in R. If you have never worked with `targets` or built the pipeline in the [engagement data harmonization repository](https://github.com/CUAHSI/engagement-data-harmonization) before, please refer the the `README` file in that repository for first time setup instructions.

**Local setup**

-   Fork the [engagement data harmonization repository](https://github.com/CUAHSI/engagement-data-harmonization) and clone that fork to your local machine
-   Create a new branch that will house any manual edits that were made to the pipeline code
-   Place the Heap exports in the folder `07_adhoc/in/`

**Manual edits to make before running the pipeline**

*Note: There will likely be other troubleshooting that occurs when generating a new report since this code is still in development.*

-   Change the date range in target `p7_heap_export_daterange` ([found here](https://github.com/CUAHSI/engagement-data-harmonization/blob/4fba7a54667cb1e85c5da130e6c82ed3f12e69d9/07_adhoc.R#L460)) to match the authors requested date range.
    -   This should follow the format `YYMMDD_YYMMDD` which was used when creating and downloading the Heap exports.
-   Update the filter in target `p7_combined_analytics`.
    -   Using the pages the author contributed, add a new collection to `process_heap_export()` inside of [this `case_when()` statement](https://github.com/CUAHSI/engagement-data-harmonization/blob/4fba7a54667cb1e85c5da130e6c82ed3f12e69d9/07_adhoc/src/processing_authorship_impact_report.R#L25).
    -   Then, in target `p7_combined_analytics`, update the collection filter ([found here](https://github.com/CUAHSI/engagement-data-harmonization/blob/4fba7a54667cb1e85c5da130e6c82ed3f12e69d9/07_adhoc.R#L516)) to use your newly created collection.
-   Change the output file name of the report ([found here](https://github.com/CUAHSI/engagement-data-harmonization/blob/4fba7a54667cb1e85c5da130e6c82ed3f12e69d9/07_adhoc.R#L630))
    -   Suggested naming convention: `AIR_[collection name]_[date created].pdf`
    -   [collection name] should match the collection you created in the previous step.
    -   [date created] should be the date you generated the report following the format `YYMMDD`.
-   Change the contributor name ([found here](https://github.com/CUAHSI/engagement-data-harmonization/blob/4fba7a54667cb1e85c5da130e6c82ed3f12e69d9/07_adhoc.R#L639)) to the author that requested the report.

**Running the pipeline**

*Note: Before continuing, make sure you have completed the local setup steps*

-   Open the R project `engagement-data-harmonization.Rproj` in RStudio
-   In the console, run `targets::tar_make(c(p7_AIR_pdf, p7_move_AIR_pdfs))`
-   Once the pipeline is finished running, the report will be generated in the folder `07_adhoc\out\`

# Policies on generating authorship impact reports

Development on the Authorship Impact Report has been paused until authors have started requesting ad-hoc reports. Development can be revisited once we have a better idea of what authors are using these reports for and any feedback on what they like or don't like about the reports.

Some edits/questions that have been outlined for further development can be found in [this GitHub issue](https://github.com/CUAHSI/engagement-data-harmonization/issues/372).
