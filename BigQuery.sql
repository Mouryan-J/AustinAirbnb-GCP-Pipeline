

SELECT * FROM `fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings`

-- Price distribution by property type (excellent for box plot / bar chart)
SELECT 
  property_type,
  COUNT(*) AS listings,
  AVG(price) AS avg_price,
  MIN(price) AS min_price,
  MAX(price) AS max_price,
  APPROX_QUANTILES(price, 4)[OFFSET(1)] AS q1,
  APPROX_QUANTILES(price, 4)[OFFSET(2)] AS median_price,
  APPROX_QUANTILES(price, 4)[OFFSET(3)] AS q3
FROM `fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings`
GROUP BY property_type
ORDER BY avg_price DESC;


-- Top host neighbourhoods by number of listings
SELECT 
  host_neighbourhood,
  COUNT(*) AS num_listings
FROM `fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings`
WHERE host_neighbourhood IS NOT NULL
GROUP BY host_neighbourhood
ORDER BY num_listings DESC;

-- Neighborhood price ranking 
SELECT 
  host_neighbourhood,
  AVG(price) AS avg_price,
  COUNT(*) AS listings
FROM `fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings`
WHERE host_neighbourhood IS NOT NULL
GROUP BY host_neighbourhood
HAVING COUNT(*) > 20
ORDER BY avg_price DESC;

-- Relationship between price and accommodates (supply scaling)

SELECT 
  accommodates,
  AVG(price) AS avg_price,
  MIN(price) AS min_price,
  MAX(price) AS max_price,
  COUNT(*) AS listings
FROM `fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings`
GROUP BY accommodates
ORDER BY accommodates;

-- Price vs review rating — is better quality more expensive?

SELECT
  review_scores_rating,
  AVG(price) AS avg_price,
  COUNT(*) AS listings
FROM `fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings`
WHERE review_scores_rating IS NOT NULL
GROUP BY review_scores_rating
ORDER BY review_scores_rating DESC;


-- Hosts with many listings vs price (host professionalism indicator)
SELECT
  host_total_listings_count,
  AVG(price) AS avg_price,
  AVG(review_scores_rating) AS avg_rating,
  COUNT(*) AS listings
FROM `fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings`
GROUP BY host_total_listings_count
HAVING COUNT(*) > 10
ORDER BY host_total_listings_count DESC;


-- Super responsive hosts vs slow hosts (service reliability index)

SELECT
  host_response_time,
  AVG(host_response_rate) AS avg_response_rate,
  AVG(host_acceptance_rate) AS avg_acceptance_rate,
  AVG(review_scores_rating) AS avg_rating,
  COUNT(*) AS listings
FROM `fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings`
GROUP BY host_response_time
ORDER BY avg_response_rate DESC;


-- Price vs bathrooms/bedrooms (amenity-driven pricing)
SELECT
  bedrooms,
  bathrooms,
  AVG(price) AS avg_price,
  COUNT(*) AS listings
FROM `fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings`
GROUP BY bedrooms, bathrooms
ORDER BY bedrooms, bathrooms;

-- Review volume vs rating (trustworthiness index)

SELECT
  number_of_reviews,
  AVG(review_scores_rating) AS avg_rating,
  AVG(price) AS avg_price,
  COUNT(*) AS listings
FROM `fa25-i535-mjayasan-airbnb.airbnb_dataset.preproccessed_lisitings`
GROUP BY number_of_reviews
ORDER BY number_of_reviews DESC;

