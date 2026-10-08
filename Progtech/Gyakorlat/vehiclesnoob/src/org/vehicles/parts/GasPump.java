package org.vehicles.parts;

public abstract class GasPump {
    protected LicensePlate licensePlate;
    protected GasPump[] gasPumps;

    protected void Vehicle(LicensePlate plate, GasPump[] gaspumps){
        this.licensePlate = plate;
        this.gasPumps = gaspumps;
    }

}
