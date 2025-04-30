require "application_system_test_case"

class InventoryUnitsTest < ApplicationSystemTestCase
  setup do
    @inventory_unit = inventory_units(:one)
  end

  test "visiting the index" do
    visit inventory_units_url
    assert_selector "h1", text: "Inventory units"
  end

  test "should create inventory unit" do
    visit inventory_units_url
    click_on "New inventory unit"

    fill_in "Average price", with: @inventory_unit.average_price
    fill_in "Batch", with: @inventory_unit.batch_id
    fill_in "Department", with: @inventory_unit.department_id
    fill_in "Internal", with: @inventory_unit.internal_id
    fill_in "Name", with: @inventory_unit.name
    fill_in "Number of units", with: @inventory_unit.number_of_units
    fill_in "Price", with: @inventory_unit.price
    fill_in "Properties", with: @inventory_unit.properties
    fill_in "Quantity", with: @inventory_unit.quantity
    fill_in "Tags", with: @inventory_unit.tags
    fill_in "Total quantity", with: @inventory_unit.total_quantity
    fill_in "Upc", with: @inventory_unit.upc
    click_on "Create Inventory unit"

    assert_text "Inventory unit was successfully created"
    click_on "Back"
  end

  test "should update Inventory unit" do
    visit inventory_unit_url(@inventory_unit)
    click_on "Edit this inventory unit", match: :first

    fill_in "Average price", with: @inventory_unit.average_price
    fill_in "Batch", with: @inventory_unit.batch_id
    fill_in "Department", with: @inventory_unit.department_id
    fill_in "Internal", with: @inventory_unit.internal_id
    fill_in "Name", with: @inventory_unit.name
    fill_in "Number of units", with: @inventory_unit.number_of_units
    fill_in "Price", with: @inventory_unit.price
    fill_in "Properties", with: @inventory_unit.properties
    fill_in "Quantity", with: @inventory_unit.quantity
    fill_in "Tags", with: @inventory_unit.tags
    fill_in "Total quantity", with: @inventory_unit.total_quantity
    fill_in "Upc", with: @inventory_unit.upc
    click_on "Update Inventory unit"

    assert_text "Inventory unit was successfully updated"
    click_on "Back"
  end

  test "should destroy Inventory unit" do
    visit inventory_unit_url(@inventory_unit)
    click_on "Destroy this inventory unit", match: :first

    assert_text "Inventory unit was successfully destroyed"
  end
end
