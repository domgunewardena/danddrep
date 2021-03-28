function showCategoryRows(clickedRow) {

  let rowNumber = clickedRow.rowIndex;
  let allRows = document.getElementsByTagName('tr');

  for (i=1; i<5; i++) {
    allRows[rowNumber + i].classList.toggle('hide-me');
  }
}

function colourScores() {

  let scale = [[4,'table-danger'],[4.5,'table-warning'],[5.1,'table-success']];
  let scoreTDs = Array.from(document.getElementsByClassName('score-td'));
  let scoreCategories = ['food','service','ambience','value']

  scoreTDs.forEach(
    function(scoreTD) {

      let score = scoreTD.textContent;

      // Add titles to zero scores explaining that no guests left a review
      if (score == 0) {

        scoreTD.innerHTML = "<p title = 'No guests left a review'>-</p>"

        for (let i = 0; i < scoreCategories.length; i++) {
          // If score is for a category, show title detailing that specific category
          if (scoreTD.classList.contains(scoreCategories[i])) {
            scoreTD.innerHTML = "<p title = 'No guests left a " + scoreCategories[i] + " score'>-</p>"
          }
        }
      }
      // Add coloured table classes to TDs based on score
      else {
        for (let i = 0; i < scale.length; i++) {
          if (score < scale[i][0]) {
            scoreTD.classList.add(scale[i][1]);
          }
      }
    }
  });
}

colourScores();


// Input Filtering

function filterRestaurant(restaurantFilter) {

  console.log('Filtering table by restaurant...')

  let table = document.getElementById('reviewsTable');
  let tableRows = table.getElementsByTagName('tr');

  // Loop through all rows
  let restaurantTD, restaurantP;
  for (let i = 1; i < tableRows.length; i++) {

    restaurantTD = tableRows[i].getElementsByTagName('td')[1];
    restaurantP = restaurantTD.getElementsByTagName('p')[0];

    if (restaurantFilter === 'All Restaurants') {
      tableRows[i].classList.remove('unselected-restaurant');
    }
    else {
      if (restaurantP.innerHTML.includes(restaurantFilter)) {
        tableRows[i].classList.remove('unselected-restaurant');
      }
      else {
        tableRows[i].classList.add('unselected-restaurant');
      }
    }
  }
  console.log('Table filtered by restaurant')
}

function filterTag(tagFilter) {

  console.log('Filtering table by tag...')

  let table = document.getElementById('reviewsTable');
  let tableRows = table.getElementsByTagName('tr');

  // Loop through all rows
  let tagTD, tagP;
  for (let i = 1; i < tableRows.length; i++) {

    tagTD = tableRows[i].getElementsByTagName('td')[8];
    tagP = tagTD.getElementsByTagName('p')[0];

    if (tagFilter === 'None') {
      tableRows[i].classList.remove('unselected-restaurant');
    }
    else {
      if (tagP) {
        if (tagP.innerHTML.includes(tagFilter)) {
          tableRows[i].classList.remove('unselected-restaurant');
        }
        else {
          tableRows[i].classList.add('unselected-restaurant');
        }
      }
      else {
        tableRows[i].classList.add('unselected-restaurant');
      }
    }
  }
  console.log('Table filtered by tag')
}

function filterTagForm(tagFilter) {

  console.log('Filtering table by tag...')

  let table = document.getElementById('reviewsTable');
  let tableRows = table.getElementsByTagName('tr');
  let tagInputs;
  
  // Loop through all rows
  for (let i = 1; i < tableRows.length; i++) {

    if (tagFilter === 'None') {
      tableRows[i].classList.remove('unselected-restaurant');
    }

    else {
      tagInputs = tableRows[i].getElementsByTagName('input');
      for (let j = 1; j < tagInputs.length; j++) {
        if (tagInputs[j].name === tagFilter) {
          if (tagInputs[j].checked) {
            tableRows[i].classList.remove('unselected-restaurant');
          }
          else {
            tableRows[i].classList.add('unselected-restaurant');
          }
        }
      }
    }
  }
  console.log('Table filtered by tag')
}


function filterReview() {

  console.log('Filtering table...')

  let reviewInput = document.getElementById('reviewFilter');
  let reviewFilter = reviewInput.value.toUpperCase();
  let table = document.getElementById('reviewsTable');
  let tr = table.getElementsByTagName('tr');

  let reviewsWithSearchText = table.getElementsByClassName('has-search-text');

  // Remove all bold text from cells that contained the previous search term
  for (i = 0; i < reviewsWithSearchText.length; i++) {
    reviewsWithSearchText[i].innerHTML = reviewsWithSearchText[i].innerHTML.replace(/<strong>/g,'');
    reviewsWithSearchText[i].innerHTML = reviewsWithSearchText[i].innerHTML.replace(/<\/strong>/g,'');
  }

  // Remove search text class from cells that contained the previous search term
  while (reviewsWithSearchText.length > 0) {
    reviewsWithSearchText[0].classList.remove('has-search-text');
  }

  // Loop through all rows
  let reviewTD, reviewP;
  for (let i = 1; i < tr.length; i++) {

    reviewTD = tr[i].getElementsByTagName('td')[7];
    reviewP = reviewTD.getElementsByTagName('p')[0];

    if (reviewFilter.length === 0) {
      tr[i].classList.remove('no-search-text');
    }
    else {
      if (reviewP.innerHTML.toUpperCase().includes(reviewFilter)) {
        tr[i].classList.remove('no-search-text');
        reviewP.classList.add('has-search-text');
      }
      else {
        tr[i].classList.add('no-search-text');
      }
    }
  }

  reviewsWithSearchText = table.getElementsByClassName('has-search-text');

  let searchMask = reviewInput.value;
  let regEx = new RegExp(searchMask, "ig");
  let replaceMask = '<strong>' + reviewInput.value + '</strong>';

  for (i = 0; i < reviewsWithSearchText.length; i++) {
    reviewsWithSearchText[i].innerHTML = reviewsWithSearchText[i].innerHTML.replace(regEx, replaceMask);
  }

  console.log('Table filter complete')

}

// Filter review table by review text on pressing enter key

let enterInput = document.getElementById('reviewFilter');
enterInput.addEventListener('keyup', function(event) {
  if (event.keyCode === 13) {
    filterReview();
  }
});


function clearReviewFilter() {

  console.log('Clearing review filter...')

  let table = document.getElementById('reviewsTable');
  let tableRows = table.getElementsByTagName('tr');
  let reviewInput = document.getElementById('reviewFilter');

  // Remove all bold text from previous search
  let reviewsWithSearchText = table.getElementsByClassName('has-search-text');
  for (i = 0; i < reviewsWithSearchText.length; i++) {
    reviewsWithSearchText[i].innerHTML = reviewsWithSearchText[i].innerHTML.replace(/<strong>/g,'');
    reviewsWithSearchText[i].innerHTML = reviewsWithSearchText[i].innerHTML.replace(/<\/strong>/g,'');
  }

  // Remove all instances of search text class
  while (reviewsWithSearchText.length > 0) {
    reviewsWithSearchText[0].classList.remove('has-search-text');
  }

  reviewInput.value = ''

  for (i = 1; i < tableRows.length; i++) {
    tableRows[i].classList.remove('no-search-text');
  }

  console.log('Review filter cleared')

}

function filterBreakdown() {

  let filterValue = document.getElementById('breakdownFilter').value
  let filter = filterValue.toUpperCase();
  let jumbotrons = document.getElementsByClassName('jumbotron');

  if (filter.length > 0){
    jumbotrons[1].classList.add('hide-me');
  }
  else {
    jumbotrons[1].classList.remove('hide-me');
  }

  let tables = [
    document.getElementById('breakdownTable'),
    document.getElementById('reviewsTable'),
  ];

  let j, table, tableRows;

  // Loop through both breakdown & reviews tables
  for (j = 0; j < tables.length; j++) {

    table = tables[j];
    tableRows = table.getElementsByTagName('tr');

    let tdColumn;
    if (j === 0) {tdColumn = 0} else {tdColumn = 1}

    let td, txtValue;
    for (i = 1; i < tableRows.length; i++) {
      td = tableRows[i].getElementsByTagName('td')[tdColumn];
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().includes(filter)) {
        tableRows[i].classList.remove('unselected-restaurant');
      } else {
        tableRows[i].classList.add('unselected-restaurant');
      }

    }
  }
}


// Score Filtering

function hideFilteredRows() {

  let table = document.getElementById('reviewsTable');
  let rows = table.rows;

  for (let i = 1; i < rows.length; i++) {

    if (rows[i].getElementsByClassName('filtered-empty').length > 0) {
      rows[i].classList.add('row-has-filtered-empty-value');
    }
    else {
      rows[i].classList.remove('row-has-filtered-empty-value');
    }
  }
}

function filterColumn(columnIndex) {

  let table = document.getElementById('reviewsTable');
  let rows = table.rows;
  let td;

  for (let i = 1; i < rows.length; i++) {

    td = rows[i].getElementsByTagName('td')[columnIndex];

    if (td.classList.contains('empty')) {
      td.classList.add('filtered-empty');
    }
    else {
      td.classList.remove('filtered-empty');
    }
  }

  hideFilteredRows();

}

function unfilterColumn(columnIndex) {

  let table = document.getElementById('reviewsTable');
  let rows = table.rows;
  let td;

  for (let i = 1; i < rows.length; i++) {
    td = rows[i].getElementsByTagName('td')[columnIndex];
    td.classList.remove('filtered-empty');
  }

  hideFilteredRows();

}

// sorting

function getValue(row, columnIndex, dataType) {
  let value = row.getElementsByTagName("td")[columnIndex].innerText;
  if (value === '-') {value = '6';}
  if (dataType === 'text') {value = value.toLowerCase();}
  else if (dataType === 'number') {value = Number(value1);}
  return value
}

function swap(rows, leftIndex, rightIndex) {
  let temp = rows[leftIndex];
  rows[leftIndex] = rows[rightIndex];
  rows[rightIndex] = rows[leftIndex];
}

function partition(rows, left, right, columnIndex, dataType) {
  let pivot = Math.floor((right + left) / 2)
  let i = left;
  let j = right;

  let pivotValue = getValue(rows[pivot], columnIndex, dataType);
  let iValue = getValue(rows[i], columnIndex, dataType);
  let jValue = getValue(rows[j], columnIndex, dataType);

  while (i <= j) {
    while (iValue < pivotValue) {
      i++;
      iValue = getValue(rows[i], columnIndex, dataType);
    }
    while (jValue > pivotValue) {
      j--;
      jValue = getValue(rows[j], columnIndex, dataType);
    }
    if (i <= j) {
      swap(rows, i, j);
      i++;
      iValue = getValue(rows[i], columnIndex, dataType);
      j++;
      jValue = getValue(rows[j], columnIndex, dataType);
    }
  }
  return i;
}

function quickSort(rows, left, right, columnIndex, dataType) {
  let index;
  if (rows.length > 1) {
    index = partition(rows, left, right, columnIndex, dataType);
    if (left < index - 1) {
      quickSort(rows, left, index - 1, columnIndex, dataType);
    }
    if (index < right) {
      quickSort(rows, right, index, columnIndex, dataType);
    }
  }
}

function sortColumn(columnIndex, dataType) {
  let rows = document.getElementById("reviewsTable").rows;
  quickSort(rows, 0, rows.length, columnIndex, dataType);
}

function sortColumnOld(columnIndex, dataType) {

  console.log('Starting column sort...')

  let table = document.getElementById("reviewsTable");
  let rows = table.rows;
  let i, value1, value2, x, y, shouldSwitch;

  let switching = true;

  while (switching) {

    switching = false;

    for (i = 1; i < (rows.length - 1); i++) {

      console.log('Checking row ' + i + '...')

      shouldSwitch = false;

      value1 = rows[i].getElementsByTagName("td")[columnIndex].innerText;
      value2 = rows[i + 1].getElementsByTagName("td")[columnIndex].innerText;

      if (value1 === '-') {value1 = '6';}
      if (value2 === '-') {value2 = '6';}

      if (dataType === 'text') {
        x = value1.toLowerCase();
        y = value2.toLowerCase();
      }
      else if (dataType === 'number') {
        x = Number(value1);
        y = Number(value2);
      }

      if (x > y) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }

  console.log('Finished sorting column')
}

function clickFilterColumn(thElement, columnIndex, dataType) {

  thElement.classList.toggle('clicked');

  if (thElement.className.includes('clicked')) {
    thElement.style.backgroundColor = '#b8daff';
    filterColumn(columnIndex);
  }
  else {
    thElement.style.backgroundColor = 'black';
    unfilterColumn(columnIndex);
  }
}

// Filter review table by category from clicking categoy score in breakdown jumbotron
function filterStat(restaurant, category) {

  let categoriesDict = {
    'food':0,
    'service':1,
    'ambience':2,
    'value':3,
  };

  let filterColumns = document.getElementsByClassName('filter-column')

  // Remove any current category filters
  for (let i = 0; i < filterColumns.length; i++) {
    if (filterColumns[i].classList.contains('clicked')) {
      filterColumns[i].click();
    }
  }

  if (category != 'total') {
    // Filter by category of stat
    let filterColumnIndex = categoriesDict[category];
    let thElement = filterColumns[filterColumnIndex];
    thElement.click();
  }

  let restaurantSelect = document.getElementById('restaurantFilter');
  restaurantSelect.value = restaurant;
  filterRestaurant(restaurant);

  let reviewsTable = document.getElementById('reviewsTable');
  reviewsTable.scrollIntoView();

}

// Change displayed scores in scores table when clicking on category
function changeScoreCategory(clickedButton) {

  let categoryButtons = document.getElementsByClassName('category-button');
  let categoryRows = document.getElementsByClassName('category-row');

  let oldClickedButton = document.getElementsByClassName('btn-primary')[0];
  let oldClickedCategory = oldClickedButton.innerHTML;
  let oldDisplayedRows = document.getElementsByClassName('category-' + oldClickedCategory)

  let clickedCategory = clickedButton.innerHTML;
  let newDisplayedRows = document.getElementsByClassName('category-' + clickedCategory)

  if (oldClickedCategory != clickedCategory) {

    oldClickedButton.classList.remove('btn-primary');
    oldClickedButton.classList.add('btn-light');

    clickedButton.classList.remove('btn-light');
    clickedButton.classList.add('btn-primary');

    for (i=0; i<oldDisplayedRows.length; i++) {
      oldDisplayedRows[i].classList.add('hide-me')
      newDisplayedRows[i].classList.remove('hide-me')
    }
  }
}

function toggleTextDisplay(element) {

  let content = element.parentElement.parentElement.getElementsByClassName('content')[0];
  let linkText = element.text.toUpperCase();

  if (linkText === "SHOW MORE"){
      linkText = "Show less";
      content.classList.remove("hideContent");
      content.classList.add("showContent");
  } else {
      linkText = "Show more";
      content.classList.remove("showContent");
      content.classList.add("hideContent");
  };

  element.text = linkText

  return false;

}

function showCheckBoxes(element) {

  let checkbox = element.parentElement.getElementsByClassName('checkboxes')[0];
  let linkText = element.getElementsByTagName('a')[0].text.toUpperCase();

  if (linkText === 'SHOW TAGS') {
    linkText = "Hide Tags";
  } else {
    linkText = "Show Tags";
  }

  checkbox.classList.toggle('hide-checkbox')
  checkbox.classList.toggle('show-checkbox')

}

// $('.selecter').selectpicker();

// document.getElementsByClassName('show-more').on("click", function() {
//
//     let content = $(this).parent().prev("div.content")[0];
//     let linkText = $(this).text().toUpperCase();
//
//     if(linkText === "SHOW MORE"){
//         linkText = "Show less";
//         content.classList.remove("hideContent");
//         content.classList.add("showContent");
//     } else {
//         linkText = "Show more";
//         content.classList.remove("showContent");
//         content.classList.add("hideContent");
//     };
//
//     $(this).text(linkText);
// });

// Archive

// function filterRestaurant() {
//
//   let input, filter, table, tr, td, i, txtValue;
//   input = document.getElementById('restaurantFilter');
//   filter = input.value.toUpperCase();
//   table = document.getElementById('reviewsTable');
//   tr = table.getElementsByTagName('tr');
//
//   for (i = 0; i < tr.length; i++) {
//     td = tr[i].getElementsByTagName('td')[1];
//     if (td) {
//       txtValue = td.textContent || td.innerText;
//       if (txtValue.toUpperCase().includes(filter)) {
//         tr[i].style.display = "";
//       } else {
//         tr[i].style.display = "none";
//       }
//     }
//   }
// }
//
// function filterReview() {
//
//   let input, filter, table, tr, td, i;
//   input = document.getElementById('reviewFilter');
//   filter = input.value.toUpperCase();
//   table = document.getElementById('reviewsTable');
//   tr = table.getElementsByTagName('tr');
//
//   for (i = 0; i < tr.length; i++) {
//     td = tr[i].getElementsByTagName('td')[7];
//     if (td) {
//       td.innerHTML = td.innerHTML.replace('<strong>','')
//       td.innerHTML = td.innerHTML.replace('</strong>','')
//       if (td.innerHTML.toUpperCase().includes(filter)) {
//         tr[i].style.display = "";
//         td.innerHTML = td.innerHTML.replace(input.value, '<strong>' + input.value + '</strong>')
//       } else {
//         tr[i].style.display = "none";
//       }
//     }
//   }
// }
//
// function filterScore(n) {
//   let input, filter, table, tr, td, i, scoreValue;
//   input = document.getElementsByClassName('scoreInput')[n];
//   filter = parseInt(input.value);
//   table = document.getElementById('reviewsTable');
//   tr = table.getElementsByTagName('tr');
//
//   for (i = 0; i < tr.length; i++) {
//     td = tr[i].getElementsByTagName('td')[3+n];
//     if (td) {
//       scoreValue = parseInt(td.textContent) || parseInt(td.innerText);
//       if (scoreValue <= filter) {
//         tr[i].style.display = "";
//       } else {
//         tr[i].style.display = "none";
//       }
//     }
//   }
// }

// function filterTable() {
//
//   let restaurantInput, restaurantFilter, reviewInput, reviewFilter, table, tr, restaurantTD, reviewTD, i;
//
//   restaurantInput = document.getElementById('restaurantFilter');
//   restaurantFilter = restaurantInput.value.toUpperCase();
//   reviewInput = document.getElementById('reviewFilter');
//   reviewFilter = reviewInput.value.toUpperCase();
//
//   table = document.getElementById('reviewsTable');
//   tr = table.getElementsByTagName('tr');
//
//   for (i = 1; i < tr.length; i++) {
//
//     restaurantTD = tr[i].getElementsByTagName('td')[1].getElementsByTagName('p')[0];
//     reviewTD = tr[i].getElementsByTagName('td')[7].getElementsByTagName('p')[0];
//
//     if (restaurantFilter.length > 0 && reviewFilter.length === 0) {
//       if (restaurantTD.innerHTML.toUpperCase().includes(restaurantFilter)) {
//         tr[i].style.display = "";
//       } else {
//         tr[i].style.display = "none";
//       }
//     } else if (restaurantFilter.length === 0 && reviewFilter.length > 0) {
//       if (reviewTD.innerHTML.toUpperCase().includes(reviewFilter)) {
//         tr[i].style.display = "";
//       } else {
//         tr[i].style.display = "none";
//       }
//     } else if (restaurantFilter.length > 0 && reviewFilter.length > 0) {
//       if (restaurantTD.innerHTML.toUpperCase().includes(restaurantFilter) && reviewTD.innerHTML.toUpperCase().includes(reviewFilter)) {
//         tr[i].style.display = "";
//       } else {
//         tr[i].style.display = "none";
//       }
//     } else {
//       tr[i].style.display = "";
//     }
//   }
// }

// function clearReviewFilter() {
//
//   console.log('Clearing review filter...')
//
//   let table = document.getElementById('reviewsTable');
//   let tr = table.getElementsByTagName('tr');
//   let reviewInput = document.getElementById('reviewFilter');
//
//   // Remove all bold text from previous search
//   let reviewsWithSearchText = table.getElementsByClassName('has-search-text');
//   for (i = 0; i < reviewsWithSearchText.length; i++) {
//     reviewsWithSearchText[i].innerHTML = reviewsWithSearchText[i].innerHTML.replace(/<strong>/g,'');
//     reviewsWithSearchText[i].innerHTML = reviewsWithSearchText[i].innerHTML.replace(/<\/strong>/g,'');
//   }
//
//   // Remove all instances of search text class
//   while (reviewsWithSearchText.length > 0) {
//     reviewsWithSearchText[0].classList.remove('has-search-text');
//   }
//
//   reviewInput.value = ''
//
//   // Check for restaurant filter
//   let restaurantFilter = document.getElementById('restaurantFilter').value;
//   let restaurantTD, restaurantP
//
//   for (i = 1; i < tr.length; i++) {
//
//     if (restaurantFilter != 'All Restaurants') {
//
//       restaurantTD = tr[i].getElementsByTagName('td')[1];
//       restaurantP = restaurantTD.getElementsByTagName('p')[0];
//
//       if (restaurantP.innerHTML.includes(restaurantFilter)) {
//         tr[i].style.display = "";
//       }
//       else {
//         tr[i].style.display = "none";
//       }
//     }
//     else {
//       tr[i].style.display = "";
//     }
//   }
//
//   console.log('Review filter cleared')
//
// }

// function filterHighlightReviewTable() {
//
//   console.log('Filtering table...')
//
//   let restaurantInput = document.getElementById('restaurantFilter');
//   let reviewInput = document.getElementById('reviewFilter');
//   let restaurantFilter = restaurantInput.value.toUpperCase();
//   let reviewFilter = reviewInput.value.toUpperCase();
//
//   let table = document.getElementById('reviewsTable');
//   let tr = table.getElementsByTagName('tr');
//   let reviewsWithSearchText = table.getElementsByClassName('has-search-text');
//
//   // Remove all bold text from cells that contained the previous search term
//   for (i = 0; i < reviewsWithSearchText.length; i++) {
//     reviewsWithSearchText[i].innerHTML = reviewsWithSearchText[i].innerHTML.replace(/<strong>/g,'');
//     reviewsWithSearchText[i].innerHTML = reviewsWithSearchText[i].innerHTML.replace(/<\/strong>/g,'');
//   }
//
//   // Remove search text class from cells that contained the previous search term
//   while (reviewsWithSearchText.length > 0) {
//     reviewsWithSearchText[0].classList.remove('has-search-text');
//   }
//
//   // Loop through all rows
//   let restaurantTD, restaurantP, reviewTD, reviewP;
//   for (let i = 1; i < tr.length; i++) {
//
//     restaurantTD = tr[i].getElementsByTagName('td')[1];
//     restaurantP = restaurantTD.getElementsByTagName('p')[0];
//     reviewTD = tr[i].getElementsByTagName('td')[7];
//     reviewP = reviewTD.getElementsByTagName('p')[0];
//
//     // No Filters
//     if (restaurantFilter === 'ALL RESTAURANTS' && reviewFilter.length === 0) {
//       // Display all rows
//       tr[i].style.display = "";
//     }
//     // Restaurant Filter
//     else if (restaurantFilter != 'ALL RESTAURANTS' && reviewFilter.length === 0) {
//       // If review is for queried restaurant
//       if (restaurantP.innerHTML.toUpperCase().includes(restaurantFilter)) {
//         // Display review
//         tr[i].style.display = "";
//       }
//       // If review isn't for queried restaurant
//       else {
//         // Hide review
//         tr[i].style.display = "none";
//       }
//     }
//     // Review Filter
//     else if (restaurantFilter === 'ALL RESTAURANTS' && reviewFilter.length > 0) {
//       // If review text contains queried text
//       if (reviewP.innerHTML.toUpperCase().includes(reviewFilter)) {
//         // Display review
//         tr[i].style.display = "";
//         // Add search text class to cell
//         reviewP.classList.add('has-search-text');
//       }
//       // If review text does not contain queried text
//       else {
//         //
//         tr[i].style.display = "none";
//       }
//     }
//     // Restaurant & Review Filter
//     else if (restaurantFilter != 'ALL RESTAURANTS' && reviewFilter.length > 0) {
//       // If review is for queried restaurant and review text contains queried text
//       if (restaurantP.innerHTML.toUpperCase().includes(restaurantFilter) && reviewP.innerHTML.toUpperCase().includes(reviewFilter)) {
//         // Display review
//         tr[i].style.display = "";
//         // Add search text class to cell
//         reviewP.classList.add('has-search-text');
//       } else {
//         // Hide review
//         tr[i].style.display = "none";
//       }
//     }
//   }
//
//   reviewsWithSearchText = table.getElementsByClassName('has-search-text');
//
//   let searchMask = reviewInput.value;
//   let regEx = new RegExp(searchMask, "ig");
//   let replaceMask = '<strong>' + reviewInput.value + '</strong>';
//
//   for (i = 0; i < reviewsWithSearchText.length; i++) {
//     // Add strong tags around search term
//     reviewsWithSearchText[i].innerHTML = reviewsWithSearchText[i].innerHTML.replace(regEx, replaceMask);
//   }
//
//   console.log('Table filter complete')
//
// }
