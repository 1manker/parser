--Lucas Manker
--Cosc 3015
--11/1/18

module Parser where

    import Data.Char

    newtype Parser a  = MkP(String ->  [(a,String)])

    data BinOp = Add | Times
       deriving Show

    data Exp = Const Int | BinExp BinOp Exp Exp
       deriving Show

    parse :: Parser a -> String -> [(a,String)]
    parse (MkP f) i = f i

    fullParse :: Parser a -> String -> a
    fullParse p  = fst . head . (parse  p)

    instance Functor Parser where
       fmap g p = MkP (\s -> map (\(v,s') ->  (g v, s')) (parse p s))

    instance Applicative Parser where
    -- pure :: a -> Parser a
      pure v = MkP (\s -> [(v,s)])

    -- <*> :: Parser (a -> b) -> Parser a -> Parser b
      pg <*> px = MkP f
         where f s =
                 let m = parse pg s in
                   concat $  map (\(g,out) -> parse (fmap g px) out) m


    instance Monad Parser where

    -- (>>=) :: Parser a -> ( a -> Parser b) -> Parser b
        p >>= q = MkP f
           where f s = case  parse p s of
                    [] -> []
                    m -> concat $  map (\(v,out) -> parse (q v) out) m

     -- return :: a -> Parser a
        return  = pure

    failure :: Parser a
    failure = MkP(\i -> [])
    zero = failure

    item :: Parser Char
    item = MkP(\i -> case i of
                     [] -> []
                     (x:xs) -> [(x,xs)])

    p :: Parser (Char,Char)

    p =  do x <- item
            item
            y <- item
            return (x,y)

    plus :: Parser a -> Parser a -> Parser a
    p `plus` q = MkP f
      where f s = parse p s ++ parse q s

    (+++) :: Parser a -> Parser a -> Parser a
    p +++ q = MkP(\i -> case parse p i of
                        [] -> parse q i
                        m -> m)



    sat :: (Char -> Bool) -> Parser Char
    sat p = do x <- item
               if p x then return x else failure

    digit  :: Parser Char
    digit  = sat (\c -> c `elem` ['0'..'9'])


    lower  :: Parser Char
    lower  =  sat (\c -> c `elem` ['a'..'z'])

    upper  :: Parser Char
    upper  = sat (\c -> c `elem` ['A'..'Z'])

    letter :: Parser Char
    letter = (lower +++ upper)

    alphanum :: Parser Char
    alphanum = (letter +++ digit)
    char      :: Char -> Parser Char
    char x = sat (==x)

    string :: String -> Parser String
    string [] = return []
    string (x:xs) = do char x
                       string xs
                       return (x:xs)

    many :: Parser a -> Parser [a]
    many p = some p +++ return []

    some :: Parser a -> Parser [a]
    some p = do v <- p
                vs <- many p
                return (v:vs)

    ident :: Parser String
    ident = do x <- lower
               xs <- many alphanum
               return (x:xs)


    identupper :: Parser String
    identupper = do x <- upper
                    xs <- many alphanum
                    return (x:xs)

    nat :: Parser Int
    nat = do xs <- some digit
             return (read xs)

    space :: Parser ()
    space = do many (char ' ')
               return ()

    token :: Parser a -> Parser a
    token p = do space
                 v <- p
                 space
                 return v

    identifier :: Parser String
    identifier = token ident

    natural :: Parser Int
    natural = token nat

    symbol :: String -> Parser String
    symbol xs = token (string xs)


    natlist :: Parser [Int]
    natlist = do symbol "["
                 n <- natural
                 ns <- many (do symbol ","
                                natural)
                 symbol "]"
                 return (n:ns)

    intp :: Parser Int
    intp = do symbol "("
              symbol "-"
              n <- natural
              symbol ")"
              return (-n)
              +++ natural

    expr :: Parser Int
    expr = do t <- term
              do symbol "+"
                 e <- expr
                 return (t + e)  
                 +++ return t                


    term :: Parser Int
    term = do f <- factor
              do symbol "*"
                 t <- term
                 return (f * t)
                 +++ return f

    factor :: Parser Int
    factor = do symbol "("
                e <- expr
                symbol ")"
                return e
                +++ natural

    expr' :: Parser Exp
    expr' = do t <- term'
               do symbol "+"
                  e <- expr'
                  return (BinExp Add t e)  
                 +++ return t 

    term' :: Parser Exp
    term' = do f <- factor'
               do symbol "*"
                  t <- term'
                  return (BinExp Times f t)
                +++ return f

    constant :: Parser Exp
    constant = do k <- natural 
                  return (Const k)

    factor' :: Parser Exp
    factor' = do symbol "("
                 e <- expr'
                 symbol ")"
                 return e
                +++ constant


