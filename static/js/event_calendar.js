// 캘린더
const es = document.getElementById("es").value;
// console.log(es);
// console.log(typeof es);
// console.log(es.includes("2022-06-12"));
// var len = Object.keys(es).length / 3;
// const dateArray = new Array();
// for(var j=0; j<len; j++){
//     dateArray.push(es["start_at"+j.toString()]);
// }

let date = new Date();

const renderCalender = () => {
  const viewYear = date.getFullYear();
  const viewMonth = date.getMonth();

  document.querySelector('.year-month').textContent = `${viewYear}년 ${viewMonth + 1}월`;

  const prevLast = new Date(viewYear, viewMonth, 0);
  const thisLast = new Date(viewYear, viewMonth + 1, 0);

  const PLDate = prevLast.getDate();
  const PLDay = prevLast.getDay();

  const TLDate = thisLast.getDate();
  const TLDay = thisLast.getDay();

  const prevDates = [];
  const thisDates = [...Array(TLDate + 1).keys()].slice(1);
  const nextDates = [];

  if (PLDay !== 6) {
    for (let i = 0; i < PLDay + 1; i++) {
      prevDates.unshift(PLDate - i);
    }
  }

  for (let i = 1; i < 7 - TLDay; i++) {
    nextDates.push(i);
  }

  const dates = prevDates.concat(thisDates, nextDates);
  const firstDateIndex = dates.indexOf(1);
  const lastDateIndex = dates.lastIndexOf(TLDate);

  dates.forEach((date, i) => {
    var month = viewMonth + 1;
    month = month < 10 ? '0' + month : '' + month;
    var cDate = date < 10 ? '0' + date : '' + date;
    var clickDate = viewYear.toString()+"-"+month.toString()+"-"+cDate.toString();
    if (es.includes(clickDate)){
        const condition = i >= firstDateIndex && i < lastDateIndex + 1
                        ? 'this'
                        : 'other';
        dates[i] = `<div class="date"><a href="javascript:openPop(${viewYear}, ${viewMonth}, ${date})" style="float=left;"><span class="${condition} activation">${date}</span></a></div>`;
    }
    else{
        const condition = i >= firstDateIndex && i < lastDateIndex + 1
                          ? 'this'
                          : 'other';
        dates[i] = `<div class="date"><a href="javascript:openPop(${viewYear}, ${viewMonth}, ${date})"><span class=${condition}>${date}</span></a></div>`;
    }  
});

  document.querySelector('.dates').innerHTML = dates.join('');
  const today = new Date();
  if (viewMonth === today.getMonth() && viewYear === today.getFullYear()) {
    for (let date of document.querySelectorAll('.date')) {
      if (+date.innerText === today.getDate()) {
        date.classList.add('today');
        break;
      }
    }
  }
};

renderCalender();

const prevMonth = () => {
//   date.setDate(1);
  date.setMonth(date.getMonth() - 1);
  renderCalender();
};

const nextMonth = () => {
  date.setMonth(date.getMonth() + 1);
  renderCalender();
};

const goToday = () => {
  date = new Date();
  renderCalender();
};


// // 팝업
// function openPop(cYear, cMonth, cDate){
//     document.getElementById("popup_layer").style.display = "block";
//     document.querySelector('.click-date').textContent = `${cYear}년 ${cMonth+1}월 ${cDate}일`;
// };
// function closePop(){
//     document.getElementById("popup_layer").style.display = "none";
// };