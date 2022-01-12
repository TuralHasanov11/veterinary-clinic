Vue.filter('truncateStr', function (value) {
    if(value && value.length>0){
        return value.substring(0,15)+'...'
    }

    return null
})


let inventoryApp = new Vue({
    el: "#inventoryApp",

    data: {
        url:'/inventory/equipment/list?page=1',

        equipment:null,
        equipmentCount:null,
        
        perPage:null,
        nextPage:null,
        prevPage:null,
        currentPage:null,
        currentPageNum:null,
        totalPages:null,
        firstPage:null,
        lastPage:null,
        pagination:null,

        loading:false,

        selectedItem:null,
        item:{
            name:null,
            quantity:null,
            price:null
        },

        searchQuery:null,
        orderByColumn:'name',
        orderDirection:1,

        success:false,
        error:false,
        successMessage:null,
        errorMessage:null,
        validationErrors:{},
    },

    created(){
        this.getEquipment(`${this.url}&ordering=${this.orderByColumn}`)
    },

    methods:{
        getEquipment(url){
            this.loading=true
            
            fetchData(url)
                .then(data => {
                    this.equipment = data.results
                    this.perPage= data.per_page
                    this.equipmentCount = data.count
                    this.nextPage = data.links.next
                    this.prevPage = data.links.previous
                    this.currentPageNum = data.current_page
                    this.totalPages = data.total_pages
                    this.firstPage = data.links.first
                    this.lastPage = data.links.last
                    this.currentPage = data.links.current
                                        
                    this.loading=false
                    
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        createEquipment(url=''){
            this.loading=true
            fetchData(`/inventory/equipment/create`, method='POST', this.item)
                .then(data => {
                    
                    this.equipment.unshift(data.item)

                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        editEquipment(url=''){
            this.loading=true

            fetchData(`/inventory/equipment/${this.selectedItem.id}`, method='POST', this.selectedItem)
                .then(data => {
                    this.equipment.splice(this.equipment.findIndex((el)=>{
                        return el.id == data.item.id
                    }), 1, data.item)

                    this.handleSuccess(data)
                   
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        deleteEquipment(url=''){
            this.loading=true
            fetchData(`/inventory/equipment/${this.selectedItem.id}/delete`, method='POST')
                .then(data => {
                    this.equipment.splice(this.equipment.findIndex((el)=>{
                        return el.id == this.selectedItem.id
                    }),1)

                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                })
        },


        filtering(){
            let url = this.url

            if(this.searchQuery){
                url+=`&search=${this.searchQuery}`
            }

            if(this.orderByColumn){
                if(this.orderDirection){
                    url+=`&ordering=${this.orderByColumn}`
                }else{
                    url+=`&ordering=-${this.orderByColumn}`
                }
            }

            this.getEquipment(url)
        },

        orderBy(column='name'){
            
            
            if(column == this.orderByColumn){
                this.orderDirection=Number(!this.orderDirection)
            }else{
                this.orderDirection = 1
                
            }

            this.orderByColumn = column

            this.filtering()

        },

        selectEquipment(item){
            this.reset()
            this.clearMessages()
            this.selectedItem = item
        },

        clearMessages(){
            this.success=false
            this.error=false
            this.errorMessage=null
            this.successMessage=null
        },

        handleSuccess(data){
            this.reset()
            this.clearMessages()
            this.loading=false
            this.success = true
            this.successMessage = data.message
        },

        handleError(data){
            this.clearMessages()
            this.loading=false

            data=JSON.parse(data.message)
            if(data.message){
                this.reset()
                this.error = true
                this.errorMessage = data.message
            }else{
                this.validationErrors = data
            }
        },

        reset(){
            this.selectedItem=null
            this.validationErrors={}
            document.querySelectorAll('.btn-close').forEach((el)=>{
                el.click()
            });
        }
    },

    // filters: {
    //     truncateStr: function (value) {
    //       if (!value) return ''
    //       value = value.toString()
    //       return value.charAt(0).toUpperCase() + value.slice(1)
    //     }
    // }
});