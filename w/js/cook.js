"use strict";
window.COOK_THEORY_FILE_SFX = ',.txt'
window.LENGHTY_RECIPE_FILE_SFX = '..txt'
window.DESSERT_FILE_SFX = ';.txt'
window.MEAL_FILE_SFX = '_.txt'

function getRecipes(numOfMeals) {
  const baseUrl = getBaseUrl()
  const filePathsFilePath = '/search_file_paths.txt'
  const searchFileUrls = getFileUrls(baseUrl, filePathsFilePath)
  const links = getRandomMealRecipes(numOfMeals, searchFileUrls)
  let recipes = ' &nbsp; '
  for (let i in links) {
    if (i > 0) {
      recipes += ' &ndash; '
    }
    recipes += links[i]
  }
  return recipes
}

function getRandomMealRecipes(numOfMeals, searchFileUrls) {
  if (window.DEBUG) console.log('*getRandomMealRecipes() searchFileUrls= ' + searchFileUrls);
  const mealUrls = getFoodFileType(searchFileUrls, window.MEAL_FILE_SFX)
  if (window.DEBUG) console.log('*getRandomMealRecipes() mealUrls= ' + mealUrls);
  const n = mealUrls.length
  let randomMeals = []
  for (let i = 0; i < numOfMeals; i++) {
    if (window.DEBUG) console.log('*getRandomMealRecipes() i= ' + i);
    let j = Math.floor(Math.random() * n)
    if (window.DEBUG) console.log('*getRandomMealRecipes() i= ' + i + ' j= ' + j);
    const link = _getShortLink(mealUrls[j])
    if (randomMeals.includes(link)) {
      i--;
    } else {
      randomMeals[i] = _getShortLink(mealUrls[j])
    }
  }
  if (window.DEBUG) console.log('*getRandomMealRecipes() randomMeals= ' + randomMeals);
  return randomMeals
}


function getFoodFileType(searchFileUrls, sfx) {
  if (sfx != window.COOK_THEORY_FILE_SFX &&
    sfx != window.LENGHTY_RECIPE_FILE_SFX &&
    sfx != window.DESSERT_FILE_SFX &&
    sfx != window.MEAL_FILE_SFX) {
    throw ' Invalid file sfx: ' + sfx;
  }
  let fileUrls = []
  let j = 0
  for (var i in searchFileUrls) {
    const url = searchFileUrls[i]
    if (url.includes('food')) {
      if (url.includes(sfx)) {
        fileUrls[j++] = url
      }
    }
  }
  if (window.DEBUG) console.log('*getFoodFileTypel() fileUrls= ' + fileUrls);
  return fileUrls
}

function _getUrlLinkLabel(url) {
  const i1 = url.lastIndexOf('/') + 1;
  let label = url.substring(i1);
  label = label.replace(/_/g, ' ').replace('.txt', '')
  return label;
}

function _getShortLink(url) {
  const label = _getUrlLinkLabel(url)
  const link = '<a href="' + url + '">' + label + '</a>'
  return link;
}
