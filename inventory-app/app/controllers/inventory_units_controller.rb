class InventoryUnitsController < ApplicationController
  before_action :set_inventory_unit, only: %i[ show edit update destroy ]
  skip_before_action :verify_authenticity_token, only: [:create]

  # GET /inventory_units or /inventory_units.json
  def index
    @inventory_units = InventoryUnit.all
  end

  # GET /inventory_units/1 or /inventory_units/1.json
  def show
  end

  # GET /inventory_units/new
  def new
    @inventory_unit = InventoryUnit.new
  end

  # GET /inventory_units/1/edit
  def edit
  end

  # POST /inventory_units/batch
  # POST /inventory_units or /inventory_units.json
  def create
    Rails.logger.info "Received inventory units batch request with params: #{params.inspect}"
    
    # Handle both direct inventory_units parameter and _json parameter
    units_data = if params[:inventory_units].is_a?(Array)
      params[:inventory_units]
    elsif params[:inventory_units].is_a?(Hash)
      params[:inventory_units].values
    elsif params[:_json]
      params[:_json]
    else
      []
    end

    batch_id = SecureRandom.uuid
    processed_units = []
    skipped_units = []

    # Calculate batch statistics first
    number_of_units = units_data.size
    average_price = units_data.sum { |u| u[:price].to_f } / number_of_units
    total_quantity = units_data.sum { |u| u[:quantity].to_i }

    units_data.each do |unit_params|
      permitted_params = unit_params.permit(
        :upc, 
        :price, 
        :quantity, 
        :department_id, 
        :internal_id, 
        :name, 
        tags: [],
        properties: [:department, :vendor, :description]
      ).merge(batch_id: batch_id)

      # Check if unit with same UPC exists
      if InventoryUnit.where(upc: permitted_params[:upc]).exists?
        skipped_units << permitted_params[:upc]
        next
      end

      unit = InventoryUnit.new(permitted_params)
      unit.build_batch_stats(
        number_of_units: number_of_units,
        average_price: average_price,
        total_quantity: total_quantity
      )

      if unit.save
        processed_units << unit
      else
        skipped_units << permitted_params[:upc]
      end
    end
    
    respond_to do |format|
      format.html { 
        redirect_to inventory_units_path, 
        notice: "Successfully processed #{processed_units.size} units. Skipped #{skipped_units.size} duplicate units." 
      }
      format.json { 
        render json: {
          batch_id: batch_id,
          processed_count: processed_units.size,
          skipped_count: skipped_units.size,
          skipped_upcs: skipped_units,
          batch_stats: {
            number_of_units: number_of_units,
            average_price: average_price,
            total_quantity: total_quantity
          }
        }, 
        status: :created 
      }
    end
  end

  # PATCH/PUT /inventory_units/1 or /inventory_units/1.json
  def update
    respond_to do |format|
      if @inventory_unit.update(inventory_unit_params)
        format.html { redirect_to @inventory_unit, notice: "Inventory unit was successfully updated." }
        format.json { render :show, status: :ok, location: @inventory_unit }
      else
        format.html { render :edit, status: :unprocessable_entity }
        format.json { render json: @inventory_unit.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /inventory_units/1 or /inventory_units/1.json
  def destroy
    @inventory_unit.destroy!

    respond_to do |format|
      format.html { redirect_to inventory_units_path, status: :see_other, notice: "Inventory unit was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_inventory_unit
      @inventory_unit = InventoryUnit.find(params[:id])
    end

    # Only allow a list of trusted parameters through.
    def inventory_unit_params
      params.require(:inventory_unit).permit(:batch_id, :upc, :price, :quantity, :department_id, :internal_id, :name, :properties, tags: [], batch_stats: [:number_of_units, :average_price, :total_quantity])
    end
end
