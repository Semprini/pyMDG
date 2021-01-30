package my.co.sample.SampleIndustry.TestDomain;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Entity
public class Location()
{
    
    @Column (name = "name", length=100)
    private String name;
    
    @Expandable (name = "Location", expandableClass = Country.class)
    private Country Location;
    
    public String getname() {
        return name;
    }

    public void setname(String name) {
        this.name = name;
    }    
    
}