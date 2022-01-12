let examinationsApp = new Vue({
    el: "#examinationsApp",

    data: {
        url:'/animals/examinations/list',

        examinations:null,

        loading:false,

        selectedExamination:null,
        examination:{
            name:null,
            min_price:null,
            max_price:null,
            price:null,
        },

        isRange:false,
        isRangeUpdate:false,

        success:false,
        error:false,
        successMessage:null,
        errorMessage:null,
        validationErrors:{},
    },

    created(){
        this.getExaminations(`${this.url}`)
    },

    methods:{
        getExaminations(url){
            this.loading=true
            
            fetchData(url)
                .then(data => {
                    this.examinations = data.results

                    this.loading=false
                    
                })
                .catch(err => {
                    this.handleError(err)
                });
        },


        createExamination(url=''){
            this.loading=true

            if(!this.isRange){
                this.examination.min_price=this.examination.price
                this.examination.max_price=this.examination.price
            }

            fetchData(`/animals/examinations/create`, method='POST', this.examination)
                .then(data => {
                    
                    this.examinations.unshift(data.examination)

                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        editExamination(url=''){
            this.loading=true

            if(!this.isRangeUpdate){
                this.selectedExamination.min_price=this.selectedExamination.price
                this.selectedExamination.max_price=this.selectedExamination.price
            }

            fetchData(`/animals/examinations/${this.selectedExamination.id}`, method='POST', this.selectedExamination)
                .then(data => {
                    this.examinations.splice(this.examinations.findIndex((el)=>{
                        return el.id == data.examination.id
                    }), 1, data.examination)

                    this.handleSuccess(data)
                   
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        deleteExamination(url=''){
            this.loading=true

            fetchData(`/animals/examinations/${this.selectedExamination.id}/delete`, method='POST')
                .then(data => {
                    this.examinations.splice(this.examinations.findIndex((el)=>{
                        return el.id == this.selectedExamination.id
                    }),1)

                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                })
        },

        selectExamination(examination){
            this.reset()
            this.clearMessages()
            this.selectedExamination = examination

            if(typeof this.selectedExamination.price === 'number'){
                this.isRangeUpdate=false
            }else{
                this.isRangeUpdate=true
            }
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
            this.selectedExamination=null
            this.validationErrors={}
            document.querySelectorAll('.btn-close').forEach((el)=>{
                el.click()
            });
        }
    }
});




