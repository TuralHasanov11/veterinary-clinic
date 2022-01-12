
let medicinesApp = new Vue({
    el: "#medicinesApp",

    data: {
        url:'/medicines/list?page=1',

        medicines:null,
        medicinesCount:null,
        companies:null,
        
        perPage:null,
        nextPage:null,
        prevPage:null,
        currentPage:null,
        currentPageNum:1,
        totalPages:null,
        firstPage:null,
        lastPage:null,
        pagination:null,

        loading:false,

        selectedMedicine:null,

        medicine:{
            name:null,
            quantity:null,
            price:null,
            our_price:null,
            company:0
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
        this.getMedicines(`${this.url}&ordering=${this.orderByColumn}`)
        this.getCompanies(`/medicines/companies/list`)
    },

    methods:{
        getMedicines(url){
            this.loading=true
            
            fetchData(url)
                .then(data => {
                    
                    this.medicines = data.results
                    this.perPage= data.per_page
                    this.medicinesCount = data.count
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

        getCompanies(url){
            
            fetchData(url)
                .then(data => {
                    this.companies = data.results                 
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        createMedicine(url=''){
            this.loading=true
            fetchData(`/medicines/create`, method='POST', this.medicine)
                .then(data => {
                    data.medicine.company= this.companies.find((el)=>{
                        return el.id===data.medicine.company
                    })
                    this.medicines.unshift(data.medicine)
                    
                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        editMedicine(url=''){
            this.loading=true
            this.selectedMedicine.company=this.selectedMedicine.company.id
                       
            fetchData(`/medicines/${this.selectedMedicine.id}`, method='POST', this.selectedMedicine)
                .then(data => {
                    data.medicine.company= this.companies.find((el)=>{
                        return el.id===data.medicine.company
                    })

                    this.medicines.splice(this.medicines.findIndex((el)=>{
                        return el.id == data.medicine.id
                    }), 1, data.medicine)

                    this.handleSuccess(data)
                   
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        deleteMedicine(url=''){
            this.loading=true

            fetchData(`/medicines/${this.selectedMedicine.id}/delete`, method='POST')
                .then(data => {
                    this.medicines.splice(this.medicines.findIndex((el)=>{
                        return el.id == this.selectedMedicine.id
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

            this.getMedicines(url)
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

        selectMedicine(medicine){
            this.reset()
            this.clearMessages()
            this.selectedMedicine = medicine
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
            this.selectedMedicine=null
            this.validationErrors={}
            document.querySelectorAll('.btn-close').forEach((el)=>{
                el.click()
            });
        }
    }
});