json.extract! inventory_unit, :id, :batch_id, :upc, :price, :quantity, :department_id, :internal_id, :name, :properties, :tags, :created_at, :updated_at
json.batch_stats do
  json.number_of_units inventory_unit.batch_stats.number_of_units
  json.average_price inventory_unit.batch_stats.average_price
  json.total_quantity inventory_unit.batch_stats.total_quantity
end
json.url inventory_unit_url(inventory_unit, format: :json)
