<template>
  <div id="tab-list-3" class="basic-tab-contents clearfix">
  	<transition name="modal">
      <ui-dialog :dialogData="dialogData" v-if='dialogShow' @ok='dialogOk' @cancel="dialogCancel"></ui-dialog>
    </transition>
    <div class="cate_prologue">
      <strong>광고 계정에 사용된 픽셀 이벤트를 매핑해 주세요.</strong>
      <p>픽셀 이벤트를 매핑해 주시면, 좀 더 편리한 맞춤 타겟팅을 사용할 수 있습니다.</p>
    </div>
    <div class="event_mapping_wrap">
      <ul>
        <li v-for="(pixelMappingCategory, index) in pixelMappingCategories" :key="index" class="select_btn">
          <div class="select_title">{{ pixelMappingCategory.title }}</div>
          <div class="select_contents">
            <div><ui-select @exceptSelectedItems="exceptSelectedItems" :selectData="pixelMappingCategory.select" :data-key="index" :onClick="multiSelect"></ui-select></div>
          </div>
        </li>
      </ul>
      <div class="btn_wrap">
        <button type="button" class="before_btn" @click="backToNeoAccountLinkage()">이전</button>
        <button class="next_btn" @click="setPixelEventMapping()">완료</button>
      </div>
    </div>
  </div>
</template>

<script>
import Select from '@/components/ui/Select'
import Dialog from '@/components/ui/Dialog'

export default {
	components:{
		'ui-select': Select,
		'ui-dialog':Dialog
	},

  created() {
		// 픽셀 맵핑 카테고리 목록
		this.$http.get('/pixel_mapping_category/')
		.then(res => {
			let categoryCount = res.data.count
			const data = res.data.data

			for(let i = 0; i < categoryCount; i++) {
				this.pixelMappingCategories.push({
					id: data[i].id,
					title: data[i].category_label_kr,
					number: i,
					key: i,
					select: {
						// select 속성이 없을때 childe vue의 selectData.default()가 호출 됨
						emptyText: this.defaultPixelEvent,
						textList: ['미지정']
					}
				})
      }
    })
  },

  beforeUpdate () {
    if(this.emptyTextId !== 0) {
      // 픽셀 이벤트 목록
      this.$http.get('/fb_ad_accounts/pixel_events', {
        params: {
          pixel_id: this.emptyTextId
        }
      })
      .then(res => {
        const data = res.data.data

        this.pixelMappingCategories.forEach(category => {
          for(let i = 0; i < data.length; i++) {
            category.select.textList.push(data[i].name)
          }
          // 셀렉트 박스 정렬
          category.select.textList.sort()
        })

        return this.pixelMappingCategories
      })
      .then(pixelMappingCategories => {
        const fbAdAccountId = localStorage.getItem('fb_ad_account_id')

        if(fbAdAccountId !== 'undefined') {
          this.$http.get('/fb_ad_accounts/' + fbAdAccountId + '/')
          .then(res => {
            const data = res.data
            const pixelEventCount = data.pixel_event_mapping_count
            const pixelEventMappings = data.pixel_event_mappings

            // 카테고리 목록
            let categoryTitles = []
            pixelMappingCategories.forEach(category => {
              categoryTitles.push(category.title)
            })
            
            pixelEventMappings.forEach(pixelEvent => {
              // 카테고리 목록의 인덱스 위치를 찾아서
              const index = categoryTitles.indexOf(pixelEvent.pixel_mapping_category.category_label_kr)

              // 해당 카테고리 인덱스에 픽셀 이벤트를 맵핑 (null이면 미지정, 아니면 해당 픽셀 이벤트를 맵핑)
              if (pixelEvent.facebook_pixel_event_name === null) {
                pixelMappingCategories[index].select.emptyText = '미지정'
              } else {
                pixelMappingCategories[index].select.emptyText = pixelEvent.facebook_pixel_event_name
              }
            })
          })
        }
      })
    }
  },

  props: [
    'emptyTextId'
  ],

  data () {
		return {
			// 픽셀 이벤트 매핑
			facebookPixelEventNames: [],
			pixelMappingCategoryIds: [],
			pixelMappingCategories: [],
			defaultPixelEvent: '픽셀 이벤트를 선택해주세요.',

			dialogShow:false,
			dialogData:{
				emptyText:'sample',
				type:'confirm',
				mode:'sample'
			},
			nextStage:false
		}
  },

  methods: {
  	dialogOpen(emptyText, type, mode) {
      this.dialogData['emptyText'] = emptyText
      this.dialogData['type'] = type
      this.dialogData['mode'] = mode
      this.dialogShow = true;
    },
    dialogOk() {
      const mode = this.dialogData.mode

      //모드별 동작
      if(mode === 'mapping') {
      	this.$emit('setPixelEventMapping', this.facebookPixelEventNames, this.pixelMappingCategoryIds)
      }
      this.nextStage = true
      this.dialogShow = false;
    },
    dialogCancel() {
      this.nextStage = false;
      this.dialogShow = false;
    },


    multiSelect (item, index) {
			// 해당 pixelMappingCategory의 pixelEvent를 변경하기 위함
			const key = event.target.closest('.select_btn').getAttribute('data-key')
			this.pixelMappingCategories[key].select.emptyText = item
		},

    backToNeoAccountLinkage () {
      let currentStep = [false, true, false]
      this.$emit('backToNeoAccountLinkage', currentStep)
    },

    setPixelEventMapping () {
			for(let i = 0; i < this.pixelMappingCategories.length; i++) {
				// 선택된 픽셀 이벤트
				let selectedPixelEvent = this.pixelMappingCategories[i].select.emptyText

				this.facebookPixelEventNames.push(selectedPixelEvent === '미지정' ? null : selectedPixelEvent)
				this.pixelMappingCategoryIds.push(this.pixelMappingCategories[i].id)
			}

			if(this.facebookPixelEventNames.includes(this.defaultPixelEvent)) {
				// 선택되지 않은 픽셀 이벤트가 있을 경우
				//컨펌,얼럿 텍스트 - 메세지창 타입(confirm,alert) - 독립적모드이름(alert 메세지시 사용 X)
        this.dialogOpen('모든 항목이 매칭되지 않았습니다.', 'alert')
			} else {
				this.dialogOpen('현재 매칭된 상태로 Target Pick 설정을 진행할까요?', 'confirm', 'mapping')
			}
    },

    // 선택한 항목을 셀렉트 박스에서 제외
    exceptSelectedItems (selectedItem, unselectedItem) {
      // console.log('선택됨: ' + selectedItem + ', 해제됨: ' + unselectedItem)

      if(unselectedItem === this.defaultPixelEvent) {
        // 이미 설정되어있는 항목들 셀렉트 박스에서 제거
        this.pixelMappingCategories.forEach(category => {
          // 이미 설정되어 있는 항목이 미지정이 아닌 경우에만 셀렉트 박스에서 제거
          if (selectedItem !== '미지정') {
            let index = category.select.textList.indexOf(selectedItem)
            
            // 중복 제거가 되는 것을 방지
            if (index > -1) {
              category.select.textList.splice(index, 1)
            }
          }
        })
      } else {
        // 선택한 항목 셀렉트 박스에 추가, 해제된 항목 셀렉트 박스에서 제거
        this.pixelMappingCategories.forEach(category => {
          // 해제된 항목이 미지정이 아닌 경우에만 셀렉트 박스에 추가
          if (unselectedItem !== '미지정') {
            category.select.textList.push(unselectedItem)
          }

          if (selectedItem !== '미지정') {
            // 선택된 항목이 미지정인 경우에는 셀렉트 박스에서 제거하지 않음
            let index = category.select.textList.indexOf(selectedItem)

            // 중복 제거가 되는 것을 방지
            if(index > -1) {
              category.select.textList.splice(index, 1)
            }
          }

          category.select.textList.sort()
        })
      }
    }
  }
}
</script>

<style>

</style>
