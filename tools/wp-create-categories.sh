#!/bin/bash
# Create missing WordPress categories via deploy.php gateway
# Run: bash tools/wp-create-categories.sh

DEPLOY_URL="https://www.sourovdeb.com/deploy.php"
DEPLOY_KEY="0767044896thevenet_"

# PHP code to create categories
PHP_CODE='<?php
require("wp-load.php");

$categories = [
    "ELT Masterclass" => "Complete 60-day English teaching course",
    "ELT" => "General English language teaching",
    "CELTA" => "CELTA certification topics",
    "Job Hunting" => "Job search and career advice",
    "AI Tools" => "AI tools and automation",
    "Teaching Resources" => "Lesson plans and materials",
    "Personal" => "Personal reflections and life",
];

$results = [];
foreach ($categories as $name => $desc) {
    $exists = term_exists($name, "category");
    if ($exists) {
        $results[] = "✓ $name (already exists)";
    } else {
        $result = wp_insert_term($name, "category", ["description" => $desc]);
        if (is_wp_error($result)) {
            $results[] = "✗ $name: " . $result->get_error_message();
        } else {
            $results[] = "✓ Created: $name (id=" . $result["term_id"] . ")";
        }
    }
}

echo json_encode(["success" => true, "results" => $results]);
?>'

# Encode to base64
ENCODED=$(echo "$PHP_CODE" | base64 -w 0)

echo "📂 Creating missing categories via deploy gateway..."
echo ""

curl -X POST "$DEPLOY_URL?key=$DEPLOY_KEY" \
  --data-urlencode "action=run_php" \
  --data-urlencode "encoded=true" \
  --data-urlencode "code=$ENCODED" \
  2>/dev/null | python3 -m json.tool

echo ""
echo "✓ Categories creation request sent."
echo "  Check WordPress admin → Posts → Categories to verify"
