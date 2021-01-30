package my.co.sample.SampleIndustry.TestDomain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class Country()
{
    
    @Id
    @Column (name = "name", length=100)
    private String name;
    
    @Expandable (name = "Countrys", expandableClass = Region.class)
    private Region Countrys;
    
    public String getname() {
        return name;
    }

    public void setname(String name) {
        this.name = name;
    }    
    
}