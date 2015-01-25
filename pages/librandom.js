/* librandom - some functions to deal with pseudorandom numbers */

function randomItem(array) {
    /* <array>
    
    Fetches a random item from <array>.*/
    rnd = Math.floor(Math.random() * array.length)
    return array[rnd];
}

function randInt(min, max) {
    /* <min> <max>
    
    Fetches a random integer between <min> and <max>.*/
    rnd = Math.floor(Math.random() * (max - min + 1)) + min;
    console.log("min = " + min + ", max = " + max + ", Picking " + rnd)
    if (rnd > max) {
        console.warn("Random value " + rnd + " is greater than " + max + "?!")
    } else if (rnd < min) {
        console.warn("Random value " + rnd + " is less than " + min + "?!")
    }
    return rnd;
}
 
function randRange(min, max) {
    /* <min> <max>
    
    Fetches a random number between <min> and <max>.*/
    rnd = Math.random() * (max - min) + min;
    if (rnd > max) {
        console.warn("Random value " + rnd + " is greater than " + max + "?!")
    } else if (rnd < min) {
        console.warn("Random value " + rnd + " is less than " + min + "?!")
    }
    console.log("min = " + min + ", max = " + max + ", Picking " + rnd)
    return rnd;
}