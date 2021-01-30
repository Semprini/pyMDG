package my.co.sample.SampleIndustry.TestDomain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class Employee()
{
    
    @Column (name = "firstName", length=100)
    private String firstName;
    
    @Column (name = "lastName", length=100)
    private String lastName;
    
    @Id
    @Column (name = "id")
    private int id;
    
    public String getfirstName() {
        return firstName;
    }

    public void setfirstName(String firstName) {
        this.firstName = firstName;
    }    
    
    public String getlastName() {
        return lastName;
    }

    public void setlastName(String lastName) {
        this.lastName = lastName;
    }    
    
    public int getid() {
        return id;
    }

    public void setid(int id) {
        this.id = id;
    }    
    
}