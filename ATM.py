import pymongo

class ATM:
    client=pymongo.MongoClient("mongodb://localhost:27017")
    db=client["ATM_DB"]
    col_client=db["Client"]
    col_bal=db["Balance"]
    def __init__(self) -> None:
        self.select=0
        self.CustPin=0
        self.CustAge=0
        self.CustAdhaar=0
        self.intial_bal=0.0
        self.CustContact=0
        self.CustEmail=""
        self.CustfName=""
        self.Custgender=0
        self.CustlName=""
        self.custAcctype=""
        self.amount=0.0
        self.curBal=0.0
        self.savingBal=0.0
    def getDataFromDB(self,val):
        self.ls=list(self.col_bal.find({"adhaar":self.CustAdhaar}))
        for self.i in self.ls:
            for self.key, self.val in self.i.items():
                if self.key=='Account_Type' and self.val=='Current':
                    for self.key1, self.val1 in self.i.items():
                        if self.key1=='balance':
                            return float(self.val1)
                            
                else:
                    for self.key1, self.val1 in self.i.items():
                        if self.key1=='balance':
                            return float(self.val1)
        return 0
    def getAccType(self):
        self.ls=list(self.col_client.find({"adhaar":self.CustAdhaar}))
        for self.i in self.ls:
            for self.key, self.val in self.i.items():
                if self.key=='Account_Type' and self.val=='Current':
                    return self.val         
                if self.key=='Account_Type' and self.val=='Saving':
                    return self.val

    def getUpdateBal(self):
        self.ls=list(self.col_bal.find({"adhaar":self.CustAdhaar}))
        for self.i in self.ls:
            for self.key, self.val in self.i.items():
                if self.val=='Current':
                    for self.key1, self.val1 in self.i.items():
                        if self.key1=='balance':
                            return float(self.val1)
                            
                else:
                    for self.key1, self.val1 in self.i.items():
                        if self.key1=='balance':
                            return float(self.val1)

    def clientInput(self):
        self.data={'fname':self.CustfName,
        'lname':self.CustlName,
        'email':self.CustEmail,
        'adhaar':self.CustAdhaar,
        'age':self.CustAge,
        'gender':self.Custgender,
        'contact':self.CustContact,
        'clientPin':self.CustPin,
        'balance':self.intial_bal,
        'Acctype':self.custAcctype
        }
        self.col_client.insert_one(self.data)
    def balanceUpdate(self):
        if self.col_bal.count_documents({'adhaar':self.CustAdhaar})==0:
            if self.custAcctype=="Current":
                self.data={'adhaar':self.CustAdhaar,
                'Account_Type':self.custAcctype,
                'balance':self.intial_bal}
                self.col_bal.insert_one(self.data)
            else:
                self.data={'adhaar':self.CustAdhaar,
                'Account_Type':self.custAcctype,
                'balance':self.intial_bal}
                self.col_bal.insert_one(self.data)
        else:
            self.ls=list(self.col_bal.find({"adhaar":self.CustAdhaar}))
            for self.i in self.ls:
                for self.key, self.val in self.i.items():
                    if self.key=='Account_Type' and self.val=='Current':
                        for self.key1, self.val1 in self.i.items():
                            if self.key1=='balance':
                                self.col_bal.update_one({'balance':self.getDataFromDB(self.CustAdhaar)},{"$set":{'balance':self.curBal}})
                                
                    else:
                        for self.key1, self.val1 in self.i.items():
                            if self.key1=='balance':
                                self.col_bal.update_one({'balance':self.getDataFromDB(self.CustAdhaar)},{"$set":{'balance':self.savingBal}})

    

    
    def setPin(self,CustPin):
        self.CustPin=CustPin
        return self.CustPin
    def checkCustAdhaarPresent(self,CustAdhar):
        if self.col_client.count_documents({"adhaar":self.CustAdhaar})!=0:
            return True
        return False
    def getCustPin(self):
        return self.CustPin
    def getCurrentBal(self):
        self.curBal=self.getDataFromDB(self.CustAdhaar)
        return self.curBal
    def getSavingBal(self):
        self.savingBal=self.getDataFromDB(self.CustAdhaar)
        return self.savingBal
    def calCurWithdraw(self,amount):
        self.curBal=self.getDataFromDB(self.CustAdhaar)
        self.curBal=self.curBal-amount
        return self.curBal
    def calCurDeposite(self,amount):
        self.curBal=self.getDataFromDB(self.CustAdhaar)
        self.curBal=self.curBal+amount
        return self.curBal
    def calSavingWithdraw(self,amount):
        self.savingBal=self.getDataFromDB(self.CustAdhaar)
        self.savingBal=self.savingBal-amount
        return self.savingBal
    def calSavingDeposit(self,amount):
        self.savingBal=self.getDataFromDB(self.CustAdhaar)
        self.savingBal=self.savingBal+amount
        return self.savingBal   
    def getCurDepositeInput(self):
        print("Current Account Balance : ",self.getCurrentBal())
        self.amount=int(input("Amount you want to withdraw from Current Account : "))
        if (self.amount+self.curBal)>=0:
            self.calCurDeposite(self.amount)
            self.balanceUpdate()
            print("New Current Account Balance  : ",self.getCurrentBal())
        else:
            print("Balance cannot be negative ")
    def getCurWithdrawInput(self):
        print("Current Account Balance : ",self.getCurrentBal())
        self.amount=float(input("Amount you want to Withdraw in Current Account : "))
        
        if (self.curBal-self.amount)>=0:
            self.calCurWithdraw(self.amount)
            self.balanceUpdate()
            print("New Current Account Balance  : ",self.getCurrentBal())
        else:
            print("Balance cannot be negative ")
    def getSavingDepositInput(self):
        print("Saving Account Balance : ",self.getSavingBal())
        self.amount=float(input("Amount you want to Deposit from Saving Account : "))
        if (self.amount+self.savingBal)>=0:
            self.calSavingDeposit(self.amount)
            self.balanceUpdate()
            print("New Saving Account Balance  : ",self.getSavingBal())
        else:
            print("Balance cannot be negative ")
    def getSavingWithdrawInput(self):
        print("Saving Account Balance : ",self.getSavingBal())
        self.amount=float(input("Amount you want to Withdraw in Saving Account : "))
        
        if (self.curBal+self.amount)>=0:
            self.calSavingWithdraw(self.amount)
            self.balanceUpdate()
            print("New Saving Account Balance  : ",self.getSavingBal())
        else:
            print("Balance cannot be negative ")

    def getCurrent(self):
        print("******Current Account Menu******")
        print("1. View Balance")
        print("2. Withdraw Funds")
        print("3. Deposit Funds")
        print("4. Exit")
        print("Enter your choice :")
        self.select=int(input())
        if self.select==1:
            print("Current Account Balance :",self.getCurrentBal())
        elif self.select==2:
            self.getCurWithdrawInput()
        elif self.select==3:
            self.getCurDepositeInput()
        elif self.select==4:
            exit()
        else:
            print("Invalid Choice :")
    def getSaving(self):
        print("******Saving Account Menu******")
        print("1. View Balance")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Exit")
        print("Enter your choice :")
        self.select=int(input())
        if self.select==1:
            print("Savings Account Balance :",self.getSavingBal())
        elif self.select==2:
            self.getSavingWithdrawInput()
        elif self.select==3:
            self.getSavingDepositInput()
        elif self.select==4:
            exit()
        else:
            print("Invalid Choice :")
    
    def optionMenu(self):
        print("***********Welcome to Indian Bank ATM***********")
        print("Select Account Type :")
        print("1. Current Account")
        print("2. Savings Account")
        print("3. Exit")
        self.select=int(input("Enter your choice :"))
        if self.select==1:
            self.getCurrent()
        elif self.select==2:
            self.getSaving()
        elif self.select==3:
            exit()
        else:
            print("Invalid Choice ")
    def signIn(self):
        self.count=0
        while(self.count<3):
            self.CustAdhaar=int(input("User Adhaar Card :"))
            self.custPin=int(input("User Pin :"))
            if self.col_client.count_documents({"adhaar":self.CustAdhaar})>0 and self.col_client.count_documents({"clientPin":self.custPin})>0:
                self.optionMenu()
                break
            else:
                print("Invalid User ID or Pin ")
            self.count+=1
    def signUP(self):
        self.CustfName=input("Enter User First Name :")
        self.CustlName=input("Enter User Last Name :")
        self.Custgender=input("Enter Your Gender :")
        self.CustAge=int(input("Enter Your Age :"))
        self.CustEmail=input("Enter Your Email :")
        
        self.CustAdhaar=int(input("Enter Your Adhaar Card Number :"))
        self.flag=True
        while self.flag:
            if self.checkCustAdhaarPresent(self.CustAdhaar):
                print("Please Re-enter Your ! Adhaar Number already exists")
                self.adharNo=int(input("Enter Your Adhaar Card Number :"))
                self.CustAdhaar=self.adharNo
            else:
                self.flag=False
        self.CustContact=int(input("Enter Your Contact Number :"))
        self.CustPin=int(input("Enter Pin :"))
        print("Enter Account Type :\n1. Current \n2. Saving")
        self.opt=int(input())
        if self.opt==1:
            self.custAcctype="Current"
        elif self.opt==2:
            self.custAcctype="Saving"
        else:
            print("Invalid Choice")
        print("Enter Minimum Balance :\n1. 500 Rs\n2. 1000 Rs\n3. Customise")
        self.balopt=int(input())
        if self.balopt==1:
            self.intial_bal=500
        elif self.balopt==2:
            self.intial_bal=1000
        elif self.balopt==3:
            self.intial_bal=int(input())
        else:
            print("Invalid Choice")
        self.clientInput()
        self.balanceUpdate()
        self.getLogin()
    def getLogin(self):
        print("********Welcome To ATM********")
        print("1. Sign In")
        print("2. Sign Up") #for new customer
        print("3. Exit")
        self.select=int(input("Enter your choice :"))
        if self.select==1:
            self.signIn()
        elif self.select==2:
            self.signUP()
        elif self.select==3:
            exit()
        else:
            print("Invalid Choice :")
if __name__=="__main__":
    obj=ATM()
    obj.getLogin()