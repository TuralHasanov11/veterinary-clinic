let doctorsApp = new Vue({
    el: "#doctorsApp",

    data: {
        url:'/animals/doctors/list',

        doctors:null,

        loading:false,

        selectedDoctor:null,
        doctor:{
            name:null,
        },

        success:false,
        error:false,
        successMessage:null,
        errorMessage:null,
        validationErrors:{},
    },

    created(){
        this.getDoctors(`${this.url}`)
    },

    methods:{
        getDoctors(url){
            this.loading=true
            
            fetchData(url)
                .then(data => {
                    this.doctors = data.results
                    
                    this.loading=false
                    
                })
                .catch(err => {
                    this.handleError(err)
                });
        },


        createDoctor(url=''){
            this.loading=true

            fetchData(`/animals/doctors/create`, method='POST', this.doctor)
                .then(data => {
                    
                    this.doctors.unshift(data.doctor)

                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        editDoctor(url=''){
            this.loading=true

            fetchData(`/animals/doctors/${this.selectedDoctor.id}`, method='POST', this.selectedDoctor)
                .then(data => {
                    this.doctors.splice(this.doctors.findIndex((el)=>{
                        return el.id == data.doctor.id
                    }), 1, data.doctor)

                    this.handleSuccess(data)
                   
                })
                .catch(err => {
                    this.handleError(err)
                });
        },

        deleteDoctor(url=''){
            this.loading=true

            fetchData(`/animals/doctors/${this.selectedDoctor.id}/delete`, method='POST')
                .then(data => {
                    this.doctors.splice(this.doctors.findIndex((el)=>{
                        return el.id == this.selectedDoctor.id
                    }),1)

                    this.handleSuccess(data)
                })
                .catch(err => {
                    this.handleError(err)
                })
        },


        selectDoctor(doctor){
            this.reset()
            this.clearMessages()
            this.selectedDoctor = doctor
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
            this.selectedDoctor=null
            this.validationErrors={}
            document.querySelectorAll('.btn-close').forEach((el)=>{
                el.click()
            });
        }
    }
});




