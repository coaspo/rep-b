"use strict";
function testFoodMain(baseUrl, searchFileUrls, appSearchFileUrls) {
   getFoodFileTypeTest(baseUrl, searchFileUrls)
   getRandomMealRecipesTest(appSearchFileUrls)
}


function getFoodFileTypeTest(baseUrl, searchFileUrls) {
   const expected1 = [baseUrl + "/tests/search-files/food/theory,.txt"]
   const theoryUrls = getFoodFileType(searchFileUrls, window.COOK_THEORY_FILE_SFX)
   validate('1 cook.js:getFoodFileType() theoryUrls ', expected1, theoryUrls);

   const expected2 = [baseUrl + "/tests/search-files/food/bread..txt"]
   const lenghtyRecipeUrls = getFoodFileType(searchFileUrls, window.LENGHTY_RECIPE_FILE_SFX)
   validate('2 cook.js:getFoodFileType() lenghtyRecipeUrls ', expected2, lenghtyRecipeUrls);

   const expected3 = [baseUrl + "/tests/search-files/food/dessert;.txt"]
   const dessertUrls = getFoodFileType(searchFileUrls, window.DESSERT_FILE_SFX)
   validate('3 cook.js:getFoodFileType() dessertUrls ', expected3, dessertUrls);

   const expected4 = [baseUrl + "/tests/search-files/food/egg_.txt",
   baseUrl + "/tests/search-files/food/eggs_.txt"]
   const mealUrls = getFoodFileType(searchFileUrls, window.MEAL_FILE_SFX)
   validate('4 cook.js:getFoodFileType() mealUrls ', expected4, mealUrls);
}

function getRandomMealRecipesTest(appSearchFileUrls) {
   const expected = 3
   const urls = getRandomMealRecipes(3, appSearchFileUrls).length
   validate('1 cook.js:getRandomMealRecipes() count ', expected, urls);
}