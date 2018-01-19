(function ($) {

  var agent = navigator.userAgent.toLowerCase();

  var dateRangeDays = 0;
  $.fn.dateRangeCustomPicker = function (options) {
    var $this = $(this);
    var baseEl = '#create-date';
    var $thisLayer = $(".date-rang-layer");
    var $thisBtn = $this.find(baseEl);
    var $flag = false;

    var defaultSetting = {single : false, autoClose : true}
    var setting = {
      single: options.single == undefined || options.single == '' ? defaultSetting.single : options.single,
      autoClose: options.autoClose == undefined || options.autoClose == '' ? defaultSetting.autoClose : options.autoClose
    }

    picker();
    function picker(){
      dateLayerSetting();
      btnClickEv();
    };
    function btnClickEv(){
      $thisLayer.find(".close").click(function(){
        $thisLayer.hide();
        return false;
      });
      $(baseEl).on("click", function(){
        $thisBtn.data('dateRangePicker').resetMonthsView();
        $thisLayer.show();
      });
    }

    /* 0601 */
    function reDateCal(eDate) {
      var reDate;
      if (eDate < 10) {
        reDate = '0' + eDate;
      }else{
        reDate = eDate;
      }
      return reDate;
    }
    function FixLocaleDateString(localeDate) {
        var newStr = "";
        for (var i = 0; i < localeDate.length; i++) {
            var code = localeDate.charCodeAt(i);
            if (code >= 46 && code <= 57) {
                newStr += localeDate.charAt(i);
            }
        }
        return newStr;
    }
     /* 0601 */

    function dateLayerSetting(){
      $thisBtn.dateRangePicker({
        inline:true,
        container: '.create-date-td .calendar',
        alwaysOpen:true,
        format: 'YYYY-MM-DD',
        language: 'ko',
        stickyMonths: false,
        duration: 0,
        minDays: "-1y",
        maxDays: "+0d",
        minDate: '0',
        hoveringTooltip: false,
        endDate: new Date(),
        selectForward: true,
        singleMonth: setting.single,
        setValue: function(s, s1, s2){
          $(baseEl).val(s1 + '~' + s2);
        }
      }).bind('datepicker-first-date-selected', function(event, obj){
        var stDate = new Date();
        var endDate = obj.date1;
        var btDay = (endDate.getTime() - stDate.getTime()) / (1000*60*60*24);

        /* 0601 firstDate value Start */
        var lDate = endDate.toLocaleDateString();
        if(Math.round(btDay)<=59) {
            if ( (navigator.appName == 'Netscape' && agent.indexOf('trident') != -1) || (agent.indexOf("msie") != -1)) {
              var fixLoDate = FixLocaleDateString(lDate.replace(/[ㄱ-ㅎㅏ-ㅣ가-힣]/g,'.')).replace(/\./g,'. ');
              var dateReplace = fixLoDate.replace(/\./gi,'');
              var strDate = getWeekday(dateReplace, 'click');
            }else{
              var dateReplace = lDate.replace(/\./gi,'');
               var strDate = getWeekday(lDate, 'click');
            }
            var dateArray = dateReplace.split(' ');
            var dateYy = dateArray[0];
            var dateMm = reDateCal(dateArray[1]);
            var dateDd = reDateCal(dateArray[2]);

            var dateAll = dateYy + '-' + dateMm + '-' + dateDd;

            $(baseEl).val(dateAll);
        }
        /* 0601 firstDate value End */


        if(Math.round(btDay)>59 && !$flag){
          $flag = true;
          alert("체크 맥스멈 기준 체크");
          $thisBtn.data('dateRangePicker').clear();
          $thisBtn.data('dateRangePicker').resetMonthsView();
          $this.removeClass("sel");
          $(baseEl).val('');
        }else{
          $flag = false;
        }
      }).bind('datepicker-change', function(){
        if(setting.autoClose){
          $thisLayer.hide();
          $('#next').removeAttr('disabled').addClass('is-active');
        }
      });
    }
    function getWeekday(sDate, type) {
      var txt = ""+sDate;
      if(type == 'click') {
        if ( (navigator.appName == 'Netscape' && agent.indexOf('trident') != -1) || (agent.indexOf("msie") != -1)) {
          var yy = txt.substr(0, 4);
          var mm = txt.substr(5, 2);
          var dd = txt.substr(7, 2);
        }else{
          var yy = parseInt(txt.substr(0, 4), 10);
          var mm = parseInt(txt.substr(5, 2), 10);
          var dd = parseInt(txt.substr(8), 10);
        }
      }else{
        var yy = parseInt(txt.substr(0, 4), 10);
        var mm = parseInt(txt.substr(5, 2), 10);
        var dd = parseInt(txt.substr(8), 10);
      }
      var d = new Date(yy,mm - 1, dd);
      var weekday=new Array(7);
      weekday[0]="일";
      weekday[1]="월";
      weekday[2]="화";
      weekday[3]="수";
      weekday[4]="목";
      weekday[5]="금";
      weekday[6]="토";
      return weekday[d.getDay()];
    }
  }
}(jQuery));

