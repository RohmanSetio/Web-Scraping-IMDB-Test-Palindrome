public class Main {
    public static void main(String[] args) {
        String text = "Malam";

        String temp  = "";
        for(int i=text.length()-1; i>=0; i--){
            char c = text.charAt(i);
            temp += String.valueOf(c);
        }
        
        if (text.toLowerCase().equals(temp.toLowerCase())){
            System.out.println("Text adalah Polindrome");
        }else{
            System.out.println("Text bukan Polindrome");
        }
    }
}