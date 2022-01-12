let companiesApp = new Vue({
    el: "#companiesApp",

    data: {
        url:'/medicines/companies/list',

        companies:null,

        loading:false,

        selectedCompany:null,
        company:{
            name:null,
            min_price:null,
            max_price:null,
            price:null,
        },

        isRange:false,

        success:false,
        error:false,
        successMessage:null,
        errorMessage:null,
        validationErrors:{},
    },

    created(){
        this.getCompanies(`${this.url}`)
    },

    methods:{
        getCompanies(url){
            this.loading=true
            
            fetchData(url)
                .then(data => {

                    this.companies = data.results
                    
                    this.loading=false
                    
                })
                .catch(err => {
                    this.handleError(err)
                });
        },


        createCompany(url=''){
            this.loading=true

            fetchData(`/medicines/companies/create`, method='POST', this.company)
                .then(data => {
                    
                    this.companies.unshift(data.company)

                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        editCompany(url=''){
            this.loading=true

            fetchData(`/medicines/companies/${this.selectedCompany.id}`, method='POST', this.selectedCompany)
                .then(data => {
                    this.companies.splice(this.companies.findIndex((el)=>{
                        return el.id == data.company.id
                    }), 1, data.company)

                    this.handleSuccess(data)
                   
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        deleteCompany(url=''){
            this.loading=true

            fetchData(`/medicines/companies/${this.selectedCompany.id}/delete`, method='POST')
                .then(data => {
                    this.companies.splice(this.companies.findIndex((el)=>{
                        return el.id == this.selectedCompany.id
                    }),1)

                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                })
        },


        selectCompany(company){
            this.reset()
            this.clearMessages()
            this.selectedCompany = company
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
            this.selectedCompany=null
            this.validationErrors={}
            document.querySelectorAll('.btn-close').forEach((el)=>{
                el.click()
            });
        }
    }
});




