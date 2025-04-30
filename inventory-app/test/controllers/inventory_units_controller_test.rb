require "test_helper"

class InventoryUnitsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @inventory_unit = inventory_units(:one)
  end

  test "should get index" do
    get inventory_units_url
    assert_response :success
  end

  test "should get new" do
    get new_inventory_unit_url
    assert_response :success
  end

  test "should create inventory_unit" do
    assert_difference("InventoryUnit.count") do
      post inventory_units_url, params: { inventory_unit: { average_price: @inventory_unit.average_price, batch_id: @inventory_unit.batch_id, department_id: @inventory_unit.department_id, internal_id: @inventory_unit.internal_id, name: @inventory_unit.name, number_of_units: @inventory_unit.number_of_units, price: @inventory_unit.price, properties: @inventory_unit.properties, quantity: @inventory_unit.quantity, tags: @inventory_unit.tags, total_quantity: @inventory_unit.total_quantity, upc: @inventory_unit.upc } }
    end

    assert_redirected_to inventory_unit_url(InventoryUnit.last)
  end

  test "should show inventory_unit" do
    get inventory_unit_url(@inventory_unit)
    assert_response :success
  end

  test "should get edit" do
    get edit_inventory_unit_url(@inventory_unit)
    assert_response :success
  end

  test "should update inventory_unit" do
    patch inventory_unit_url(@inventory_unit), params: { inventory_unit: { average_price: @inventory_unit.average_price, batch_id: @inventory_unit.batch_id, department_id: @inventory_unit.department_id, internal_id: @inventory_unit.internal_id, name: @inventory_unit.name, number_of_units: @inventory_unit.number_of_units, price: @inventory_unit.price, properties: @inventory_unit.properties, quantity: @inventory_unit.quantity, tags: @inventory_unit.tags, total_quantity: @inventory_unit.total_quantity, upc: @inventory_unit.upc } }
    assert_redirected_to inventory_unit_url(@inventory_unit)
  end

  test "should destroy inventory_unit" do
    assert_difference("InventoryUnit.count", -1) do
      delete inventory_unit_url(@inventory_unit)
    end

    assert_redirected_to inventory_units_url
  end
end
