// DataStatistics
//
// Class to calculate some basic values from the received data
// such as standard deviation, quantile, min, max and mean values.

module.exports = class DataStatistics {
    velocity_scalar_data;
    acceleration_scalar_data;

    constructor(jsondata){
        this.timedata = jsondata.time_data;
        this.spatial_data = jsondata.spatial_data;
        this.acceleration_data = jsondata.acceleration_data;
        this.velocity_data = jsondata.velocity_data;

        this.velocity_scalar_data = this.vectorDataToScalar(this.velocity_data);
        this.acceleration_scalar_data = this.vectorDataToScalar(this.acceleration_data);

    }

    getDimensionFromArray(array, dimension){
        var result = [];
        for (var i = 0; i < array.length; i++){
            result.push(array[i][dimension])
        }
        return [...result];
    }

    vectorDataToScalar(array){
        const scalarList = [];
        for (var i = 0; i < array.length; i++){
            const data = array[i];
            const scalar = Math.sqrt( Math.pow(data["x"],2) + Math.pow(data["y"],2) + Math.pow(data["z"],2) );
            scalarList.push(scalar);
        }

        return [...scalarList]
    }

    getStatistics(){
        const velocity_sorted = this.asc(this.velocity_scalar_data);
        const acceleration_sorted = this.asc(this.acceleration_scalar_data);

        const positionalX_data = this.getDimensionFromArray(this.spatial_data, "x");
        const positionalZ_data = this.getDimensionFromArray(this.spatial_data, "z");

        const posX_sorted = this.asc(positionalX_data);
        const posZ_sorted = this.asc(positionalZ_data);

        const statsObj = {
            velocity: {
                std: this.std(velocity_sorted),
                Q1: this.quantile(velocity_sorted, .25),
                Q2: this.quantile(velocity_sorted, .50),
                Q3: this.quantile(velocity_sorted, .75),
                min: velocity_sorted[0],
                max: velocity_sorted[velocity_sorted.length-1],
                mean: this.mean(velocity_sorted)
            },
            acceleration: {
                std: this.std(acceleration_sorted),
                Q1: this.quantile(acceleration_sorted, .25),
                Q2: this.quantile(acceleration_sorted, .50),
                Q3: this.quantile(acceleration_sorted, .75),
                min: acceleration_sorted[0],
                max: acceleration_sorted[acceleration_sorted.length-1],
                mean: this.mean(acceleration_sorted)
            },
            position: {
                xmin: posX_sorted[0],
                xmax: posX_sorted[posX_sorted.length-1],
                zmin: posZ_sorted[0],
                zmax: posZ_sorted[posZ_sorted.length-1],
            }
        }
        return statsObj;
    }

    quantile(arr, q){
        const sorted = arr;
        const pos = (sorted.length - 1) * q;
        const base = Math.floor(pos);
        const rest = pos - base;
        if (sorted[base + 1] !== undefined) {
            return sorted[base] + rest * (sorted[base + 1] - sorted[base]);
        } else {
            return sorted[base];
        }
    };

    // sorts array (to prepare for quantile calculations etc)
    asc(arr) {
        return [...arr].sort((a, b) => a - b)
    };

    sum(arr){return arr.reduce((a, b) => a + b, 0)};

    mean(arr){return this.sum(arr) / arr.length};

    std(arr){
        const mu = this.mean(arr);
        const diffArr = arr.map(a => (a - mu) ** 2);
        return Math.sqrt(this.sum(diffArr) / (arr.length - 1));
    };


}