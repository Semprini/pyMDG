package my.co.sample.SampleIndustry.TestDomain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class Department()
{
    
    @Column (name = "departmentName", length=100)
    private String departmentName;
    
    @Id
    @Column (name = "id")
    private int id;
    
    @Expandable (name = "Departments", expandableClass = Location.class)
    private Location Departments;
    
    @Expandable (name = "Departments", expandableClass = Employee.class)
    private Employee Departments;
    
    public String getdepartmentName() {
        return departmentName;
    }

    public void setdepartmentName(String departmentName) {
        this.departmentName = departmentName;
    }    
    
    public int getid() {
        return id;
    }

    public void setid(int id) {
        this.id = id;
    }    
    
}