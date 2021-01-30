package my.co.sample.SampleIndustry.TestDomain2;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class Region()
{
    
    @Id
    @Column (name = "name", length=100)
    private String name;
    
    public String getname() {
        return name;
    }

    public void setname(String name) {
        this.name = name;
    }    
    
}