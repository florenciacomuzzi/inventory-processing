class BatchStats
  include Mongoid::Document
  field :_id, type: String, default: -> { inventory_unit.batch_id }
  field :number_of_units, type: Integer
  field :average_price, type: BigDecimal
  field :total_quantity, type: Integer
  
  embedded_in :inventory_unit
end 