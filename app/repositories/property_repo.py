from neo4j import Driver

QUERY_NEAREST = """
WITH point({latitude: $lat, longitude: $lng}) AS userLocation

MATCH (o:Owner)-[:OWNS]->(p:Property)-[:LOCATED_AT]->(l:Location)
WHERE l.location IS NOT NULL

WITH o, p,
     point.distance(l.location, userLocation) AS distanceMeters

ORDER BY distanceMeters ASC
LIMIT 1

RETURN 

// Owner Projection (API Safe)
{
  owner_id: o.owner_id,
  full_name: o.full_name,
  email: o.email,
  phone: o.phone,
  entity_type: o.entity_type,
  mailing_address: o.mailing_address,
  credit_score_est: o.credit_score_est,
  income_bracket: o.income_bracket,
  net_worth_est: o.net_worth_est,
  portfolio_size: o.portfolio_size,
  min_price_expectation: o.min_price_expectation,
  preferred_close_days: o.preferred_close_days,
  urgency_score: o.urgency_score,
  is_absentee: o.is_absentee,
  willing_to_sell: o.willing_to_sell,
  willing_to_partner: o.willing_to_partner
} AS owner,

// Property Projection (API Safe)
{
  property_id: p.property_id,
  internal_asset_code: p.internal_asset_code,
  structure_type: p.structure_type,
  listing_status: p.listing_status,
  occupancy_status: p.occupancy_status,
  property_grade: p.property_grade,
  energy_rating: p.energy_rating,

  year_built: p.year_built,
  floors_count: p.floors_count,
  bedrooms: p.bedrooms,
  bathrooms: p.bathrooms,
  total_built_sqft: p.total_built_sqft,
  lot_size_sqft: p.lot_size_sqft,
  garage_spaces: p.garage_spaces,

  purchase_price: p.purchase_price,
  expected_sale_price: p.expected_sale_price,
  market_value_est: p.market_value_est,
  current_rent: p.current_rent,
  rental_yield_percent: p.rental_yield_percent,
  vacancy_days: p.vacancy_days,
  tenant_present: p.tenant_present,

  exterior_condition: p.exterior_condition,
  foundation_type: p.foundation_type,
  roof_type: p.roof_type,
  roof_material: p.roof_material,
  roof_condition: p.roof_condition,
  roof_pitch: p.roof_pitch,
  roof_age_years: p.roof_age_years,
  siding_material: p.siding_material,
  gutter_status: p.gutter_status,
  hvac_type: p.hvac_type,
  electric_type: p.electric_type,
  plumbing_type: p.plumbing_type,
  solar_installed: p.solar_installed,

  mold_risk_level: p.mold_risk_level,
  termite_risk_level: p.termite_risk_level,
  structural_risk_level: p.structural_risk_level,
  fire_damage_flag: p.fire_damage_flag,
  water_damage_flag: p.water_damage_flag,

  created_at: toString(p.created_at),
  updated_at: toString(p.updated_at)

} AS property,

distanceMeters
"""


def find_nearest_property_and_owner(driver: Driver, lat: float, lng: float):

    with driver.session(database="neo4j") as session:
        result = session.run(
            QUERY_NEAREST,
            lat=lat,
            lng=lng
        )

        record = result.single()

        if not record:
            return None

        return {
            "owner": record["owner"],
            "property": record["property"],
            "distanceMeters": record["distanceMeters"]
        }
