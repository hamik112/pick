<template>
  <div id="main_wrap" class="clearfix">
    <Header></Header>
    <div id="container">
      <Aside></Aside>
      <div id="container_wrap">
        <div class="list-tab-widget">
          <div class="tab-contents-widget">
            <div id="section_list_2" class="section_tab_contents clearfix">
              <div class="target_contents_wrap">
                <div class="target_search_wrap clearfix">
                  <div class="cate_select">
                    <p>카테고리</p>
                    <ui-select :selectData="this.categorySelectData" :onClick="selectCategory"></ui-select>
                  </div>
                  <div class="admin_select">
                    <p>광고계정</p>
                    <ui-select :selectData="this.accountSelectData" :onClick="selectAccount"></ui-select>
                  </div>
                  <div class="data_select">
                    <p>기간</p>
                    <div class="select_btn">
                      <div class="select_contents">
                        <div class="select"><p class="calendar">오늘: 2017/11/13</p></div>
                      </div>
                    </div>
                  </div>
                  <button>검색</button>
                </div>
                <div class="target_report_wrap">
                  <div class="target_setup">
                    <div class="select_btn">
                      <div class="select_contents test01">
                        <div class="select" v-on:click="sortSelectOnOff()"><p>열 맞춤 설정</p></div>
                        <ul class="select_view test01_view" v-if="this.sortSelectData.onShow">
                          <li v-for="item in this.sortSelectData.textList"><input type="checkbox" id="sort01"><label for="sort01"></label>{{ item }}</li>
                        </ul>
                      </div>
                    </div>
                    <button>
                      <span>
                        <img src="../../assets/images/icon/excel_icon.png" alt="">
                      </span>
                      <span>엑셀로 내보내기</span>
                    </button>
                  </div>
                  <div class="target_report_contents">
                    <div class="report_contents_inner_wrap">
                      <table class="contents_inner">
                        <thead>
                          <tr>
                            <th rowspan="2">광고주</th>
                            <th rowspan="2">캠페인명</th>
                            <th rowspan="2">기간</th>
                            <th rowspan="2">광고세트</th>
                            <th rowspan="2">연령</th>
                            <th rowspan="2">성별</th>
                            <th rowspan="2">관심사 개수</th>
                            <th rowspan="2">맞춤타겟 이름</th>
                            <th rowspan="2">
                              <span>광고비</span>
                              <span class="sort_btn"></span>
                            </th>
                            <th rowspan="2">
                              <span>노출</span>
                              <span class="sort_btn"></span>
                            </th>
                            <th rowspan="2">
                              <span>도달</span>
                              <span class="sort_btn"></span>
                            </th>
                            <th rowspan="2">
                              <span>도달빈도</span>
                              <span class="sort_btn"></span>
                            </th>
                            <th colspan="3">사이트 유입 지표</th>
                            <th colspan="6">슬라이드 소재 클릭 지표</th>
                            <th colspan="6">영상캠페인 지표</th>
                            <th colspan="7">전환 지표</th>
                            <th colspan="4">페이지 참여 지표</th>
                          </tr>
                          <tr class="tbody_th">
                            <td>
                              <span>링크클릭</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>CTR</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>CPC</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>1번</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>2번</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>13번</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>4번</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>5번</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>6번</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>3초 이상 View</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>3초 이상 VTR</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>3초 이상 CPV</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>10초 이상 View</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>10초 이상 VTR</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>10초 이상 CPV</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>전환 완료</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>전환 완료 가치</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>1단계 완료</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>2단계 완료</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>3단계 완료</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>4단계 완료</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>5단계 완료</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>공유</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>좋아요</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>댓글</span>
                              <span class="sort_btn"></span>
                            </td>
                            <td>
                              <span>공감</span>
                              <span class="sort_btn"></span>
                            </td>
                          </tr>
                        </thead>
                        <tbody>
                          <tr>
                            <td>광고주</td>
                            <td>CTR</td>
                            <td>CPC</td>
                            <td>1번</td>
                            <td>2번</td>
                            <td>3번</td>
                            <td>4번</td>
                            <td>5번</td>
                            <td>6번</td>
                            <td>3초 이상 View</td>
                            <td>3초 이상 VTR</td>
                            <td>3초 이상 CPV</td>
                            <td>10초 이상 View</td>
                            <td>10초 이상 VTR</td>
                            <td>10초 이상 CPV</td>
                            <td>전환 완료</td>
                            <td>전환 완료 가치</td>
                            <td>1단계 완료</td>
                            <td>2단계 완료</td>
                            <td>3단계 완료</td>
                            <td>4단계 완료</td>
                            <td>5단계 완료</td>
                            <td>공유</td>
                            <td>좋아요</td>
                            <td>댓글</td>
                            <td>공감</td>
                            <td>10초 이상 CPV</td>
                            <td>전환 완료</td>
                            <td>전환 완료 가치</td>
                            <td>1단계 완료</td>
                            <td>2단계 완료</td>
                            <td>3단계 완료</td>
                            <td>4단계 완료</td>
                            <td>5단계 완료</td>
                            <td>공유</td>
                            <td>좋아요</td>
                            <td>댓글</td>
                            <td>공감</td>
                          </tr>
                          <tr>
                            <td>광고주</td>
                            <td>CTR</td>
                            <td>CPC</td>
                            <td>1번</td>
                            <td>2번</td>
                            <td>3번</td>
                            <td>4번</td>
                            <td>5번</td>
                            <td>6번</td>
                            <td>3초 이상 View</td>
                            <td>3초 이상 VTR</td>
                            <td>3초 이상 CPV</td>
                            <td>10초 이상 View</td>
                            <td>10초 이상 VTR</td>
                            <td>10초 이상 CPV</td>
                            <td>전환 완료</td>
                            <td>전환 완료 가치</td>
                            <td>1단계 완료</td>
                            <td>2단계 완료</td>
                            <td>3단계 완료</td>
                            <td>4단계 완료</td>
                            <td>5단계 완료</td>
                            <td>공유</td>
                            <td>좋아요</td>
                            <td>댓글</td>
                            <td>공감</td>
                            <td>10초 이상 CPV</td>
                            <td>전환 완료</td>
                            <td>전환 완료 가치</td>
                            <td>1단계 완료</td>
                            <td>2단계 완료</td>
                            <td>3단계 완료</td>
                            <td>4단계 완료</td>
                            <td>5단계 완료</td>
                            <td>공유</td>
                            <td>좋아요</td>
                            <td>댓글</td>
                            <td>공감</td>
                          </tr>
                          <tr>
                            <td>광고주</td>
                            <td>CTR</td>
                            <td>CPC</td>
                            <td>1번</td>
                            <td>2번</td>
                            <td>3번</td>
                            <td>4번</td>
                            <td>5번</td>
                            <td>6번</td>
                            <td>3초 이상 View</td>
                            <td>3초 이상 VTR</td>
                            <td>3초 이상 CPV</td>
                            <td>10초 이상 View</td>
                            <td>10초 이상 VTR</td>
                            <td>10초 이상 CPV</td>
                            <td>전환 완료</td>
                            <td>전환 완료 가치</td>
                            <td>1단계 완료</td>
                            <td>2단계 완료</td>
                            <td>3단계 완료</td>
                            <td>4단계 완료</td>
                            <td>5단계 완료</td>
                            <td>공유</td>
                            <td>좋아요</td>
                            <td>댓글</td>
                            <td>공감</td>
                            <td>10초 이상 CPV</td>
                            <td>전환 완료</td>
                            <td>전환 완료 가치</td>
                            <td>1단계 완료</td>
                            <td>2단계 완료</td>
                            <td>3단계 완료</td>
                            <td>4단계 완료</td>
                            <td>5단계 완료</td>
                            <td>공유</td>
                            <td>좋아요</td>
                            <td>댓글</td>
                            <td>공감</td>
                          </tr>
                          <tr>
                            <td>광고주</td>
                            <td>CTR</td>
                            <td>CPC</td>
                            <td>1번</td>
                            <td>2번</td>
                            <td>3번</td>
                            <td>4번</td>
                            <td>5번</td>
                            <td>6번</td>
                            <td>3초 이상 View</td>
                            <td>3초 이상 VTR</td>
                            <td>3초 이상 CPV</td>
                            <td>10초 이상 View</td>
                            <td>10초 이상 VTR</td>
                            <td>10초 이상 CPV</td>
                            <td>전환 완료</td>
                            <td>전환 완료 가치</td>
                            <td>1단계 완료</td>
                            <td>2단계 완료</td>
                            <td>3단계 완료</td>
                            <td>4단계 완료</td>
                            <td>5단계 완료</td>
                            <td>공유</td>
                            <td>좋아요</td>
                            <td>댓글</td>
                            <td>공감</td>
                            <td>10초 이상 CPV</td>
                            <td>전환 완료</td>
                            <td>전환 완료 가치</td>
                            <td>1단계 완료</td>
                            <td>2단계 완료</td>
                            <td>3단계 완료</td>
                            <td>4단계 완료</td>
                            <td>5단계 완료</td>
                            <td>공유</td>
                            <td>좋아요</td>
                            <td>댓글</td>
                            <td>공감</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                  <div class="pagination">
                    <ul>
                      <li><img src="../../assets/images/icon/paging_01.png" alt=""></li>
                      <li><img src="../../assets/images/icon/paging_03.png" alt=""></li>
                      <li class="now">1</li>
                      <li>2</li>
                      <li><img src="../../assets/images/icon/paging_04.png" alt=""></li>
                      <li><img src="../../assets/images/icon/paging_02.png" alt=""></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
// 레이아웃 호출
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import Aside from '@/components/layout/Aside'
// UI
import Select from '@/components/ui/Select'

export default {
  name: 'TargetReport',

  components: {
    'Header': Header,
    'Footer': Footer,
    'Aside': Aside,
    'ui-select': Select
  },

  data () {
    return {
      categorySelectData: {
        emptyText: '전체',
        textList: [
          '카테고리1',
          '카테고리2',
          '카테고리3'
        ]
      },
      accountSelectData: {
        emptyText: '전체',
        textList: [
          '광고계정1',
          '광고계정2',
          '광고계정3'
        ]
      },
      sortSelectData: {
        emptyText: '열 맞춤 설정',
        onShow:false,
        textList: [
          '설정1',
          '설정2',
          '설정3'
        ],
        checkId:[
          'sort1',
          'sort2',
          'sort3'
        ]
      }

    }
  },

  methods: {
    selectCategory: function (item) {
      this.categorySelectData.emptyText = item
    },
    selectAccount: function (item) {
      this.accountSelectData.emptyText = item
    },
    sortSelectOnOff:function() {
      this.sortSelectData.onShow = !this.sortSelectData.onShow
    }
  }
}
</script>

<style lang="css" scoped>
</style>
