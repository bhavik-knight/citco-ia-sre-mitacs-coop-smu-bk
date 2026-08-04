The Top K dropdown widget on the dashboard

is currently a dummy — it does not filter

widgets dynamically.

CloudWatch does not support native

cross-widget variable filtering.

## Decision

Replace SEARCH expressions in metric widgets

with Metrics Insights SQL queries that

support LIMIT for Top K filtering.

## For Each Metric Widget

Replace current SEARCH expression:

BEFORE (SEARCH):

SEARCH('{AWS/Lambda,FunctionName}

MetricName="Errors"', 'Sum', 300)

AFTER (Metrics Insights):

SELECT SUM(Errors)

FROM SCHEMA("AWS/Lambda", FunctionName)

WHERE FunctionName LIKE 'lda-%'

GROUP BY FunctionName

ORDER BY SUM() DESC

LIMIT 10

## Widgets To Update

Apply Metrics Insights queries to:

1. Error Rate widget

Metric: Errors

Order: DESC (highest errors first)

Limit: 10

2. Duration Avg widget

Metric: Duration (Average)

Order: DESC (slowest first)

Limit: 10

3. Duration Max widget

Metric: Duration (Maximum)

Order: DESC

Limit: 10

4. Throttles widget

Metric: Throttles

Order: DESC

Limit: 10

5. Concurrent Executions widget

Metric: ConcurrentExecutions

Order: DESC

Limit: 10

## Top K Values

Create 3 versions of each widget

using CloudFormation conditions:

OR better approach:

Use LIMIT 10 as default

Document that to change Top K:

- Update the LIMIT value in widget YAML

- Redeploy dashboard

## Remove Dummy Dropdown

Remove the Top K dropdown text widget

since it cannot function dynamically.

Replace with a text widget that says:

"Showing Top 10 Lambdas by metric value.

To change Top K: update LIMIT in

widget config and redeploy."

## Questions Before Implementation

1. Is Metrics Insights available in

your AWS account?

Verify by running:

aws cloudwatch get-metric-data \

--metric-data-queries \

'[{"Id":"test","Expression":

"SELECT SUM(Errors) FROM SCHEMA(\"AWS/Lambda\",FunctionName) LIMIT 5",

"Period":300}]' \

--start-time 2024-01-01T00:00:00Z \

--end-time 2024-01-02T00:00:00Z \

--profile cr_dev \

--region eu-west-1

2. What is the current default Top K value

shown in the dummy dropdown?

(5, 10, 20?)

3. Should Top K apply to ALL widgets

or only specific ones?

Answer these questions first.

Do not generate any code yet.

## Common Causes and Solutions

### 1. Empty Query String

The most common cause is an empty or whitespace-only query. Make sure your query contains actual content.

### 2. Query Formatting Issues

Try this properly formatted version of your query:

### 3. Step-by-Step Troubleshooting

Step 1: Test with a basic query first

Step 2: If that works, add the parse command

Step 3: Add filters one by one

### 4. Check Your Query Setup

Make sure you have:

Selected log groups: You need to select at least one log group before running the query

Set time range: Ensure you have a valid time range selected

Proper log group selection: Use either individual log group names or the prefix method

### 5. Alternative Query Approaches

Option A: Use exact log group names If you know the exact Lambda function names, select them individually in the log group selection.

Option B: Use log group prefix In the CloudWatch Logs Insights console:

Go to CloudWatch Logs Insights

Instead of selecting individual log groups, use Log group criteria

Add prefix:

/aws/lambda/

Then run your query

Option C: Simplified query for testing

### 6. Console vs API Issues

If you're using the AWS Console:

Try refreshing the page

Clear browser cache

Try a different browser

If you're using AWS CLI/SDK:

Ensure your query string is properly escaped

Check that you're not passing an empty string

### 7. Verify Log Group Access

Make sure you have the necessary permissions:

logs:StartQuery

logs:GetQueryResults

logs:DescribeLogGroups

Next Steps:

Start with the basic query in Step 1 above

Gradually add complexity

If you continue getting errors, please share:

The exact query you're trying to run

How you're running it (Console, CLI, SDK)

The complete error message

This will help identify the specific cause of the syntax error.

ACCEPTANCE CRITERIA EVALUATION FOR THE LAMBDA DASHBOARD